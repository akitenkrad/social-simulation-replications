#!/usr/bin/env python3
"""review-kit / convention 軸: ディレクトリ構成・命名規約の決定的チェッカ.

判断は一切しない. ルールセット (rules/*.json) に書かれた構造的制約だけを検証し,
finding.schema.json に準拠したレコードを出力する.

設計上の約束:
  - 標準ライブラリのみに依存する (フックから毎回起動されるため)
  - 何があっても異常終了しない (フックを壊すのが最悪の失敗)
  - 既定では非ブロッキング (exit 0). --block を付けたときだけ high で exit 2

使い方:
  check_conventions.py                       # リポジトリ全体を走査
  check_conventions.py --changed a.rs b.py   # 変更パスに関係するルールだけ実行 (フック用)
  check_conventions.py --format json         # JSONL 出力 (台帳・評価用)
  check_conventions.py --block               # high があれば exit 2
  check_conventions.py --selftest            # 内蔵フィクスチャで自己検査
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OVERRIDE_FILE = ".review-kit.json"

# スクリプト単独配置・review-kit/scripts/ 配置のどちらでも動くよう候補を順に探す
RULES_DIR_CANDIDATES = [
    Path(os.environ["REVIEW_KIT_RULES"]) if os.environ.get("REVIEW_KIT_RULES") else None,
    SCRIPT_DIR / "rules",
    SCRIPT_DIR.parent / "rules",
]


def resolve_rules_dir(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_dir() else None
    for cand in RULES_DIR_CANDIDATES:
        if cand and cand.is_dir():
            return cand
    return None


# --------------------------------------------------------------------------
# レコード
# --------------------------------------------------------------------------


@dataclass
class Finding:
    axis: str
    tag: str
    path: str
    severity: str
    claim: str
    replacement: str
    rule_id: str | None = None
    line: int | None = None
    rationale: str | None = None
    est_loc_delta: int | None = None
    detected_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    def to_record(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


# --------------------------------------------------------------------------
# リポジトリ操作
# --------------------------------------------------------------------------


def find_repo_root(start: Path, walk_up: bool = True) -> Path:
    cur = start.expanduser().resolve()
    if not walk_up:
        return cur
    for candidate in [cur, *cur.parents]:
        if (candidate / ".git").exists():
            return candidate
    return cur


def git_tracked(root: Path, pathspec: str) -> list[str]:
    """git が追跡しているパスを返す. git が無ければ空リスト."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--", pathspec],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    return [line for line in out.stdout.splitlines() if line.strip()]


def read_toml(path: Path) -> dict | None:
    try:
        with path.open("rb") as fh:
            return tomllib.load(fh)
    except (OSError, tomllib.TOMLDecodeError):
        return None


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


# --------------------------------------------------------------------------
# ルールセットの読み込みと選択
# --------------------------------------------------------------------------


def load_rulesets(rules_dir: Path) -> list[dict]:
    rulesets = []
    if not rules_dir.is_dir():
        return rulesets
    for p in sorted(rules_dir.glob("*.json")):
        try:
            rulesets.append(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"review-kit: ルールセットを読めません {p}: {exc}", file=sys.stderr)
    return rulesets


def select_ruleset(root: Path, rulesets: list[dict]) -> dict | None:
    """明示指定 (.review-kit.json) を最優先し, 無ければ detect で自動判定する."""
    override = root / OVERRIDE_FILE
    if override.is_file():
        try:
            pinned = json.loads(override.read_text(encoding="utf-8")).get("ruleset")
        except (OSError, json.JSONDecodeError):
            pinned = None
        if pinned:
            for rs in rulesets:
                if rs.get("id") == pinned:
                    return rs
            print(
                f"review-kit: {OVERRIDE_FILE} が指すルールセット '{pinned}' が見つかりません",
                file=sys.stderr,
            )
            return None

    best: tuple[int, dict] | None = None
    for rs in rulesets:
        detect = rs.get("detect", {})
        required = detect.get("all", [])
        forbidden = detect.get("none", [])
        if not required:
            continue
        if any(not (root / rel).exists() for rel in required):
            continue
        if any((root / rel).exists() for rel in forbidden):
            continue
        score = len(required)
        if best is None or score > best[0]:
            best = (score, rs)
    return best[1] if best else None


# --------------------------------------------------------------------------
# ルール種別ごとの検査
# --------------------------------------------------------------------------


def _sev(rule: dict, default: str = "medium") -> str:
    return rule.get("severity", default)


def _mk(rule: dict, path: str, claim: str, replacement: str, **kw) -> Finding:
    return Finding(
        axis="convention",
        tag=rule.get("tag", "misplaced"),
        rule_id=rule.get("id"),
        path=path,
        severity=_sev(rule),
        claim=claim,
        replacement=replacement,
        rationale=rule.get("rationale"),
        **kw,
    )


def check_repo_name(root: Path, rule: dict) -> list[Finding]:
    name = root.name
    pattern = rule["pattern"]
    max_len = rule.get("max_length")
    out = []
    if not re.match(pattern, name):
        out.append(
            _mk(
                rule,
                ".",
                f"リポジトリのディレクトリ名 '{name}' が規約の形式に一致しません",
                f"{pattern} に一致する名前 (例: replication-dynamic-models-of-segregation) にリネームする",
            )
        )
    elif max_len and len(name) > max_len:
        out.append(
            _mk(
                rule,
                ".",
                f"リポジトリ名が {len(name)} 文字で上限 {max_len} を超えています",
                f"意味が伝わる短縮形にして {max_len} 文字以内に収める",
            )
        )
    return out


def check_require_path(root: Path, rule: dict) -> list[Finding]:
    out = []
    for rel in rule["paths"]:
        if not (root / rel).exists():
            out.append(
                _mk(
                    rule,
                    rel,
                    f"規約が要求する {rel} が存在しません",
                    rule.get("hint", f"{rel} を作成する"),
                )
            )
    return out


def check_require_glob(root: Path, rule: dict) -> list[Finding]:
    """glob に一致するパスが 1 つ以上あることを確認する (src/{pkg}/cli.py など)."""
    out = []
    for pattern in rule["globs"]:
        if not list(root.glob(pattern)):
            out.append(
                _mk(
                    rule,
                    pattern,
                    f"{pattern} に一致するファイルがありません",
                    rule.get("hint", f"{pattern} を作成する"),
                )
            )
    return out


def check_gitignore_contains(root: Path, rule: dict) -> list[Finding]:
    gi = root / ".gitignore"
    text = read_text(gi)
    if text is None:
        return [
            _mk(
                rule,
                ".gitignore",
                ".gitignore が存在しないため, ローカル専用ファイルや実験結果が追跡されます",
                "規約の .gitignore を作成し " + ", ".join(rule["entries"]) + " を登録する",
            )
        ]
    def norm(e: str) -> str:
        # gitignore では /target/ と target/ と target は同じ対象を指す
        return e.strip().strip("/")

    lines = {
        norm(ln) for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")
    }
    out = []
    for entry in rule["entries"]:
        if norm(entry) not in lines:
            out.append(
                _mk(
                    rule,
                    ".gitignore",
                    f".gitignore に '{entry}' の行がありません",
                    f".gitignore に '{entry}' を追加する",
                )
            )
    return out


def check_forbid_tracked(root: Path, rule: dict) -> list[Finding]:
    out = []
    for spec in rule["paths"]:
        for tracked in git_tracked(root, spec):
            out.append(
                _mk(
                    rule,
                    tracked,
                    f"{tracked} が git の追跡対象になっています (規約では追跡しません)",
                    f"git rm --cached '{tracked}' で追跡を外し .gitignore を確認する",
                )
            )
    return out


RUN_DIR_TIMESTAMP_RE = re.compile(r"[0-9]{8}_[0-9]{6}")


def is_grouping_dir(d: Path) -> bool:
    """d が «実行ディレクトリを束ねるだけの階層» かを構造だけで判定する.

    直下に «タイムスタンプ名のサブディレクトリ» が 1 つ以上あれば, d 自身は 1 回の
    実行の出力先ではなく, 実行ごとの出力を束ねる階層である (schelling1971 の
    results/paper_reproduction/<ts>/ が実例). この形では再実行しても既存の結果が
    上書きされないため, 命名・記録の検査は d ではなくその子に対して行う.

    見るのはサブディレクトリ名だけで, 中身の意味は一切判定しない.
    """
    try:
        return any(c.is_dir() and RUN_DIR_TIMESTAMP_RE.search(c.name) for c in d.iterdir())
    except OSError:
        return False


def grouping_children(d: Path, exclude: set[str]) -> list[Path]:
    """まとめディレクトリ d の直下から, 検査対象となる実行ディレクトリを取り出す."""
    try:
        return sorted(
            c
            for c in d.iterdir()
            if c.is_dir() and not c.name.startswith(".") and c.name not in exclude
        )
    except OSError:
        return []


def check_child_name_pattern(root: Path, rule: dict) -> list[Finding]:
    parent = root / rule["parent"]
    if not parent.is_dir():
        return []  # gitignore 対象で存在しないのは正常
    pattern = rule["pattern"]
    out = []
    exclude = set(rule.get("exclude", []))
    grouping = rule.get("grouping_dirs", False)
    for child in sorted(parent.iterdir()):
        if child.name.startswith(".") or child.name in exclude:
            continue
        if rule.get("dirs_only", True) and not child.is_dir():
            continue
        if grouping and child.is_dir() and is_grouping_dir(child):
            targets = grouping_children(child, exclude)
        else:
            targets = [child]
        for target in targets:
            if not re.match(pattern, target.name):
                rel = str(target.relative_to(root))
                out.append(
                    _mk(
                        rule,
                        rel,
                        f"'{target.name}' が {rule['parent']} の命名規約に一致しません",
                        rule.get("hint", f"{pattern} に一致する名前にする"),
                    )
                )
    return out


def check_require_in_children(root: Path, rule: dict) -> list[Finding]:
    parent = root / rule["parent"]
    if not parent.is_dir():
        return []
    child_pat = rule.get("child_pattern", "*")
    exclude = set(rule.get("exclude", []))
    out = []
    for child in sorted(parent.iterdir()):
        if not child.is_dir() or child.name in exclude:
            continue
        if not fnmatch.fnmatch(child.name, child_pat):
            continue
        present = {p.name for p in child.iterdir()}
        # any_of: いずれか 1 つあればよい (config.json / sweep_config.json の分岐)
        for group in rule.get("any_of", []):
            if not (set(group) & present):
                rel = str(child.relative_to(root))
                out.append(
                    _mk(
                        rule,
                        rel,
                        f"{rel} に {' または '.join(group)} がありません (実験条件が記録されていません)",
                        f"{rel}/{group[0]} を出力するように実行側を修正する",
                    )
                )
        for required in rule.get("all_of", []):
            if required not in present:
                rel = str(child.relative_to(root))
                out.append(
                    _mk(
                        rule,
                        rel,
                        f"{rel} に {required} がありません",
                        f"{rel}/{required} を出力するように実行側を修正する",
                    )
                )
    return out


def _extract_name(root: Path, spec: dict) -> tuple[str | None, str]:
    """識別子の抽出. (値, 参照したパス) を返す."""
    rel = spec["path"]
    target = root / rel
    kind = spec["from"]
    if kind == "toml_package_name":
        data = read_toml(target)
        if not data:
            return None, rel
        return (data.get("project", {}) or {}).get("name") or (
            data.get("package", {}) or {}
        ).get("name"), rel
    if kind == "toml_bin_name":
        data = read_toml(target)
        if not data:
            return None, rel
        bins = data.get("bin") or []
        if isinstance(bins, list) and bins:
            return bins[0].get("name"), rel
        return None, rel
    if kind == "single_child_dir":
        if not target.is_dir():
            return None, rel
        dirs = [p.name for p in target.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))]
        return (dirs[0] if len(dirs) == 1 else None), rel
    return None, rel


def check_name_consistency(root: Path, rule: dict) -> list[Finding]:
    """paper_key を 1 箇所から取り出し, 派生名がすべて整合しているかを見る."""
    key_spec = rule["key"]
    raw, key_path = _extract_name(root, key_spec)
    if raw is None:
        return []  # 抽出できない = 対象外の構成. 判断しない
    key = raw
    suffix = key_spec.get("strip_suffix")
    if suffix and key.endswith(suffix):
        key = key[: -len(suffix)]
    out = []
    key_pattern = rule.get("key_pattern")
    if key_pattern and not re.match(key_pattern, key):
        out.append(
            _mk(
                rule,
                key_path,
                f"内部識別子 (paper_key) '{key}' が規約の形式に一致しません",
                "{筆頭著者の姓 (小文字 ASCII)}{発行年4桁} 形式にする (例: schelling1971)",
            )
        )
    for exp in rule.get("expect", []):
        actual, rel = _extract_name(root, exp)
        if actual is None:
            continue
        wanted = exp["template"].format(key=key, key_snake=key.replace("-", "_"))
        if actual != wanted:
            f = _mk(
                rule,
                rel,
                f"'{actual}' が paper_key '{key}' から導かれる名前と一致しません",
                f"'{wanted}' にリネームする",
            )
            f.tag = "inconsistent"
            out.append(f)
    return out


def check_records_run_config(root: Path, rule: dict) -> list[Finding]:
    """実行ディレクトリに機械可読な記録が残っているかを検査する.

    require モードが 2 つある.

    - "any_json" (既定): JSON が 1 つでもあれば通す. これは *決定的* に判定できる.
    - "config_content": config.json 相当か, config ブロックを持つ JSON を要求する.

    既定を "any_json" にしているのは意図的である. 「その JSON が実験条件の十分な
    記録になっているか」は意味の判断であり, 記録の形はリポジトリごとに違う
    (config ブロック / cargo_invocations / トップレベルのフラットなパラメータ).
    形を列挙して判定しようとすると誤検出が出る (実際に 2 回出した). 十分性の判断は
    repro 軸のスキルに委ね, ここでは「記録が何も無い」ことだけを確実に捕まえる.
    """
    parent = root / rule["parent"]
    if not parent.is_dir():
        return []
    exclude = set(rule.get("exclude", []))
    mode = rule.get("require", "any_json")
    config_names = set(rule.get("config_names", ["config.json", "sweep_config.json"]))
    config_key = rule.get("config_key", "config")
    max_bytes = rule.get("max_json_bytes", 8 * 1024 * 1024)

    grouping = rule.get("grouping_dirs", False)
    out = []
    targets: list[Path] = []
    for child in sorted(parent.iterdir()):
        if not child.is_dir() or child.name in exclude or child.name.startswith("."):
            continue
        if grouping and is_grouping_dir(child):
            targets.extend(grouping_children(child, exclude))
        else:
            targets.append(child)

    for child in targets:
        jsons = sorted(child.glob("*.json"))
        if mode == "any_json":
            if jsons:
                continue
            rel = str(child.relative_to(root))
            out.append(
                _mk(
                    rule,
                    rel,
                    f"{rel} に機械可読な実行記録 (JSON) がありません",
                    f"実行時に {rel}/config.json など, 条件を含む JSON を書き出す",
                )
            )
            continue

        recorded = False
        for f in jsons:
            if f.name in config_names:
                recorded = True
                break
            try:
                if f.stat().st_size > max_bytes:
                    continue
                data = json.loads(f.read_text(encoding="utf-8", errors="replace"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(data, dict) and isinstance(data.get(config_key), dict) and data[config_key]:
                recorded = True
                break
        if not recorded:
            rel = str(child.relative_to(root))
            out.append(
                _mk(
                    rule,
                    rel,
                    f"{rel} に config ブロックを持つ JSON がありません",
                    f"実行時に {rel}/config.json を書く",
                )
            )
    return out


CHECKERS = {
    "repo_name": check_repo_name,
    "require_path": check_require_path,
    "require_glob": check_require_glob,
    "gitignore_contains": check_gitignore_contains,
    "forbid_tracked": check_forbid_tracked,
    "child_name_pattern": check_child_name_pattern,
    "require_in_children": check_require_in_children,
    "records_run_config": check_records_run_config,
    "name_consistency": check_name_consistency,
}


# --------------------------------------------------------------------------
# 実行
# --------------------------------------------------------------------------


def rule_is_relevant(rule: dict, changed: list[str] | None) -> bool:
    if changed is None:
        return True
    watch = rule.get("watch")
    if not watch:
        return True  # watch 未指定のルールは常に走る
    for path in changed:
        for pat in watch:
            if fnmatch.fnmatch(path, pat):
                return True
    return False


def run(root: Path, ruleset: dict, changed: list[str] | None, trace: list | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for rule in ruleset.get("rules", []):
        rid = rule.get("id", "?")
        kind = rule.get("kind", "")
        if not rule_is_relevant(rule, changed):
            if trace is not None:
                trace.append({"id": rid, "kind": kind, "status": "SKIP", "count": 0})
            continue
        checker = CHECKERS.get(kind)
        if checker is None:
            print(f"review-kit: 未知のルール種別 {kind!r}", file=sys.stderr)
            if trace is not None:
                trace.append({"id": rid, "kind": kind, "status": "UNKNOWN", "count": 0})
            continue
        try:
            got = checker(root, rule)
        except Exception as exc:  # チェッカの不具合でフックを壊さない
            print(f"review-kit: ルール {rid} が失敗しました: {exc}", file=sys.stderr)
            if trace is not None:
                trace.append({"id": rid, "kind": kind, "status": "ERROR", "count": 0})
            continue
        findings.extend(got)
        if trace is not None:
            trace.append(
                {"id": rid, "kind": kind, "status": "NG" if got else "OK", "count": len(got)}
            )
    return findings


def render_text(findings: list[Finding], ruleset_id: str) -> str:
    if not findings:
        return f"review-kit/convention [{ruleset_id}]: 規約違反はありません."
    order = {"high": 0, "medium": 1, "low": 2}
    lines = [f"review-kit/convention [{ruleset_id}]: {len(findings)} 件"]
    for f in sorted(findings, key=lambda x: (order.get(x.severity, 9), x.path)):
        loc = f"{f.path}:{f.line}" if f.line else f.path
        lines.append(f"  [{f.severity}] {loc}")
        lines.append(f"      {f.claim}")
        lines.append(f"      → {f.replacement}")
    return "\n".join(lines)


def render_verbose(
    root: Path,
    ruleset: dict,
    trace: list,
    findings: list[Finding],
    changed: list[str] | None,
) -> str:
    detect = ruleset.get("detect", {}).get("all", [])
    lines = [
        "review-kit / convention",
        f"  root      : {root}",
        f"  ruleset   : {ruleset.get('id')}  ({ruleset.get('description', '')})",
        f"  detect    : {', '.join(detect) or '-'}",
        f"  source    : {ruleset.get('source', '-')}",
        f"  mode      : {'changed (' + ', '.join(changed) + ')' if changed else 'full scan'}",
        f"  rules     : {len(ruleset.get('rules', []))}",
        "",
        "ルール実行結果",
    ]
    for t in trace:
        mark = {"OK": "OK  ", "NG": "NG  ", "SKIP": "SKIP", "ERROR": "ERR ", "UNKNOWN": "??  "}[
            t["status"]
        ]
        suffix = f"  ({t['count']} 件)" if t["count"] else ""
        lines.append(f"  [{mark}] {t['id']:<28} {t['kind']}{suffix}")

    counts = {"high": 0, "medium": 0, "low": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    lines += [
        "",
        f"集計: high {counts['high']} / medium {counts['medium']} / low {counts['low']}"
        f"  (合計 {len(findings)} 件)",
    ]

    if findings:
        order = {"high": 0, "medium": 1, "low": 2}
        lines.append("")
        lines.append("指摘")
        for i, f in enumerate(sorted(findings, key=lambda x: (order.get(x.severity, 9), x.path)), 1):
            loc = f"{f.path}:{f.line}" if f.line else f.path
            lines.append(f"  {i}. [{f.severity}] {loc}   (rule: {f.rule_id}, tag: {f.tag})")
            lines.append(f"       claim       : {f.claim}")
            lines.append(f"       replacement : {f.replacement}")
            if f.rationale:
                lines.append(f"       rationale   : {f.rationale}")
    return "\n".join(lines)


def scan_one(
    root: Path, rulesets: list[dict], changed: list[str] | None
) -> tuple[dict | None, list[Finding], list]:
    ruleset = select_ruleset(root, rulesets)
    if ruleset is None:
        return None, [], []
    trace: list = []
    findings = run(root, ruleset, changed, trace)
    return ruleset, findings, trace


def render_aggregate(results: list[tuple[Path, dict | None, list[Finding]]]) -> str:
    """--each 用: どのルールがどれだけのリポジトリで発火したかの分布."""
    by_rule: dict[str, set[str]] = {}
    total = 0
    scanned = 0
    skipped = []
    for root, ruleset, findings in results:
        if ruleset is None:
            skipped.append(root.name)
            continue
        scanned += 1
        total += len(findings)
        for f in findings:
            by_rule.setdefault(f.rule_id or "?", set()).add(root.name)

    lines = ["", "=" * 64, f"集約: {scanned} リポジトリを走査, 指摘 {total} 件"]
    if skipped:
        lines.append(f"  対象外 ({len(skipped)}): {', '.join(sorted(skipped))}")
    lines.append("")
    lines.append("  発火リポジトリ数  ルール")
    for rule_id, repos in sorted(by_rule.items(), key=lambda kv: -len(kv[1])):
        share = f"{len(repos):>3}/{scanned}"
        note = ""
        if scanned and len(repos) == scanned:
            note = "   ← 全件発火. ルール側を疑う"
        lines.append(f"  {share}            {rule_id}{note}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="review-kit convention checker")
    ap.add_argument("--root", default=".", help="リポジトリルート (既定: カレントから .git を探索)")
    ap.add_argument("--rules-dir", default=None, help="ルールセットのディレクトリ")
    ap.add_argument(
        "--each",
        action="store_true",
        help="--root を「リポジトリが並ぶ親ディレクトリ」とみなし, 直下の各ディレクトリを個別に走査する",
    )
    ap.add_argument("--changed", nargs="*", default=None, help="変更されたパス (フック用)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("-v", "--verbose", action="store_true", help="ルール単位の実行結果まで表示")
    ap.add_argument("--block", action="store_true", help="high の指摘があれば exit 2")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    rules_dir = resolve_rules_dir(args.rules_dir)
    if rules_dir is None:
        print(
            "review-kit: ルールセットのディレクトリが見つかりません.\n"
            "  探した場所: "
            + ", ".join(str(c) for c in RULES_DIR_CANDIDATES if c)
            + "\n  --rules-dir で明示するか, 環境変数 REVIEW_KIT_RULES を設定してください.",
            file=sys.stderr,
        )
        return 3
    rulesets = load_rulesets(rules_dir)
    if not rulesets:
        print(f"review-kit: {rules_dir} に有効なルールセットがありません.", file=sys.stderr)
        return 3

    explicit_root = args.root != "."
    base = Path(args.root).expanduser().resolve()

    # --- 複数リポジトリの一括走査 -------------------------------------------
    if args.each:
        if not base.is_dir():
            print(f"review-kit: {base} はディレクトリではありません.", file=sys.stderr)
            return 3
        results: list[tuple[Path, dict | None, list[Finding]]] = []
        for child in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(".")):
            ruleset, findings, trace = scan_one(child, rulesets, args.changed)
            results.append((child, ruleset, findings))
            if args.format == "json":
                for f in findings:
                    rec = f.to_record()
                    rec["repo"] = child.name
                    print(json.dumps(rec, ensure_ascii=False))
            elif ruleset is None:
                print(f"--- {child.name}: 対象外 (どのルールセットにも一致せず)")
            elif args.verbose:
                print(f"\n{'=' * 64}\n{child.name}")
                print(render_verbose(child, ruleset, trace, findings, args.changed))
            else:
                print(f"--- {child.name}  [{ruleset.get('id')}]")
                print(render_text(findings, ruleset.get("id", "?")))
        if args.format != "json":
            print(render_aggregate(results))
        if args.block and any(f.severity == "high" for _, _, fs in results for f in fs):
            return 2
        return 0

    # --- 単一リポジトリ -----------------------------------------------------
    root = find_repo_root(base, walk_up=not explicit_root)
    ruleset, findings, trace = scan_one(root, rulesets, args.changed)

    if ruleset is None:
        # フック実行時 (--changed) は黙って通す. 手動実行では必ず理由を出す.
        if args.changed is None:
            child_hits = [
                p.name
                for p in sorted(root.iterdir())
                if p.is_dir() and not p.name.startswith(".") and select_ruleset(p, rulesets)
            ] if root.is_dir() else []
            msg = [
                f"review-kit: {root} はどのルールセットにも一致しませんでした (規約の対象外として通過).",
                f"  ルール : {rules_dir}",
                f"  候補   : {', '.join(r.get('id', '?') for r in rulesets)}",
            ]
            if child_hits:
                msg.append(
                    f"  ヒント : 直下の {len(child_hits)} 個のディレクトリは一致します "
                    f"({', '.join(child_hits[:3])}...). --each を付けてください."
                )
            print("\n".join(msg), file=sys.stderr)
        return 0

    if args.format == "json":
        for f in findings:
            print(json.dumps(f.to_record(), ensure_ascii=False))
    elif args.verbose:
        print(render_verbose(root, ruleset, trace, findings, args.changed))
    else:
        text = render_text(findings, ruleset.get("id", "?"))
        # PostToolUse では stderr が Claude に渡る
        print(text, file=sys.stderr if findings else sys.stdout)

    if args.block and any(f.severity == "high" for f in findings):
        return 2
    return 0


# --------------------------------------------------------------------------
# 自己検査: 一次指標は「正しいリポジトリで 1 件も出さないこと」
# --------------------------------------------------------------------------


def _build_clean_repo(base: Path) -> Path:
    repo = base / "replication-dynamic-models-of-segregation"
    (repo / "simulation" / "src").mkdir(parents=True)
    (repo / "tools" / "src" / "schelling1971_tools").mkdir(parents=True)
    (repo / ".claude").mkdir()
    (repo / "results" / "run_20260417_153000").mkdir(parents=True)
    (repo / "results" / "sweep_20260418_090000").mkdir(parents=True)
    (repo / ".git").mkdir()
    (repo / "simulation" / "Cargo.toml").write_text(
        '[package]\nname = "schelling1971-simulation"\nversion = "0.1.0"\n'
        '\n[[bin]]\nname = "schelling1971"\npath = "src/main.rs"\n',
        encoding="utf-8",
    )
    (repo / "tools" / "pyproject.toml").write_text(
        '[project]\nname = "schelling1971-tools"\nversion = "0.1.0"\n', encoding="utf-8"
    )
    (repo / "Cargo.toml").write_text('[workspace]\nmembers = ["simulation"]\n', encoding="utf-8")
    (repo / "pyproject.toml").write_text("[tool.uv.workspace]\nmembers = [\"tools\"]\n", encoding="utf-8")
    (repo / "README.md").write_text("# replication\n", encoding="utf-8")
    (repo / ".claude" / "CLAUDE.md").write_text("local\n", encoding="utf-8")
    (repo / ".gitignore").write_text(".claude/\n/target/\nresults/\n__pycache__/\n", encoding="utf-8")
    for d in ("run_20260417_153000", "sweep_20260418_090000"):
        name = "config.json" if d.startswith("run") else "sweep_config.json"
        (repo / "results" / d / name).write_text("{}", encoding="utf-8")
        (repo / "results" / d / "metrics.csv").write_text("step,value\n", encoding="utf-8")
    return repo


def _build_clean_rust_repo(base: Path) -> Path:
    repo = base / "replication-autodan"
    (repo / "src").mkdir(parents=True)
    (repo / "analysis").mkdir()
    (repo / "tests").mkdir()
    (repo / ".claude").mkdir()
    (repo / ".git").mkdir()
    (repo / "results" / "attack_20260417_153000").mkdir(parents=True)
    (repo / "Cargo.toml").write_text('[package]\nname = "autodan"\n', encoding="utf-8")
    for f in ("main.rs", "config.rs", "metrics.rs"):
        (repo / "src" / f).write_text("// stub\n", encoding="utf-8")
    (repo / "analysis" / "visualize.py").write_text("# stub\n", encoding="utf-8")
    (repo / "analysis" / "requirements.txt").write_text("matplotlib\n", encoding="utf-8")
    (repo / "README.md").write_text("# replication\n", encoding="utf-8")
    (repo / ".claude" / "CLAUDE.md").write_text("local\n", encoding="utf-8")
    (repo / ".gitignore").write_text(".claude/\n/target/\nresults/\n", encoding="utf-8")
    (repo / "results" / "attack_20260417_153000" / "config.json").write_text("{}", encoding="utf-8")
    (repo / "results" / "attack_20260417_153000" / "metrics.csv").write_text("k,v\n", encoding="utf-8")
    return repo


def _build_clean_python_repo(base: Path) -> Path:
    repo = base / "replication-universal-and-transferable-adversarial-attacks"
    pkg = repo / "src" / "gcg_replication"
    pkg.mkdir(parents=True)
    (repo / "scripts").mkdir()
    (repo / "configs").mkdir()
    (repo / "tests").mkdir()
    (repo / ".claude").mkdir()
    (repo / ".git").mkdir()
    (repo / "results" / "train_20260417_153000").mkdir(parents=True)
    (repo / "pyproject.toml").write_text('[project]\nname = "gcg-replication"\n', encoding="utf-8")
    for f in ("__init__.py", "cli.py", "metrics.py"):
        (pkg / f).write_text("# stub\n", encoding="utf-8")
    for f in ("run.py", "sweep.py", "visualize.py"):
        (repo / "scripts" / f).write_text("# stub\n", encoding="utf-8")
    (repo / "configs" / "default.yaml").write_text("seed: 42\n", encoding="utf-8")
    (repo / "README.md").write_text("# replication\n", encoding="utf-8")
    (repo / ".claude" / "CLAUDE.md").write_text("local\n", encoding="utf-8")
    (repo / ".gitignore").write_text(".claude/\nresults/\n__pycache__/\n", encoding="utf-8")
    (repo / "results" / "train_20260417_153000" / "config.json").write_text("{}", encoding="utf-8")
    return repo


def selftest() -> int:
    rules_dir = resolve_rules_dir(None)
    if rules_dir is None:
        print('selftest: ルールセットが見つかりません', file=sys.stderr)
        return 1
    rulesets = load_rulesets(rules_dir)
    failures: list[str] = []

    # 回帰: 実験条件が config.json 以外に記録されていても発火しないこと
    # (reproduce_summary.json の config ブロックを見落としていた実バグ)
    with tempfile.TemporaryDirectory() as td:
        repo = _build_clean_repo(Path(td))
        rs = select_ruleset(repo, rulesets)
        d = repo / "results" / "reproduce_20260530_214157"
        d.mkdir()
        (d / "reproduce_summary.json").write_text(
            json.dumps({"config": {"seed": 42, "n_agents": 80}, "mode": "mock"}), encoding="utf-8"
        )
        got = [f for f in run(repo, rs, None) if f.rule_id == "results-has-record"]
        if got:
            failures.append(f"repro-summary: config ブロックがあるのに発火 ({[f.path for f in got]})")

        # 記録の「形」が違うだけの JSON も通すこと (cargo_invocations 型 / フラット型)
        d3 = repo / "results" / "run_20260102_000000"
        d3.mkdir()
        (d3 / "reproduce_summary.json").write_text(
            json.dumps({"seed": 42, "cargo_invocations": ["cargo run -- run --n 200"]}),
            encoding="utf-8",
        )
        if [f for f in run(repo, rs, None) if f.rule_id == "results-has-record"]:
            failures.append("flat-shape: 別形式の記録があるのに発火した")

        # JSON が 1 つも無いときだけ発火すること
        d2 = repo / "results" / "run_20260101_000000"
        d2.mkdir()
        (d2 / "metrics.csv").write_text("k,v\n", encoding="utf-8")
        paths = {f.path for f in run(repo, rs, None) if f.rule_id == "results-has-record"}
        if "results/run_20260101_000000" not in paths:
            failures.append("no-config: 条件が記録されていないのに発火しませんでした")

    # 回帰: results/<name>/<ts>/ の 2 段構成を誤検出しないこと
    # (schelling1971 の results/paper_reproduction/<ts>/ が実例. まとめディレクトリ
    #  自体は 1 回の実行の出力先ではなく, 再実行で上書きされないため実害が無い)
    with tempfile.TemporaryDirectory() as td:
        repo = _build_clean_repo(Path(td))
        rs = select_ruleset(repo, rulesets)
        grp = repo / "results" / "paper_reproduction"
        (grp / "20260530_203515").mkdir(parents=True)
        (grp / "20260530_203515" / "summary.json").write_text("{}", encoding="utf-8")
        got = [
            f
            for f in run(repo, rs, None)
            if f.rule_id in ("results-dir-naming", "results-has-record")
        ]
        if got:
            failures.append(
                "grouping-clean: まとめディレクトリで発火 "
                + str([f"{f.rule_id}@{f.path}" for f in got])
            )

        # まとめディレクトリの «中» は通常どおり検査すること (記録欠落)
        (grp / "20260601_120000").mkdir()
        (grp / "20260601_120000" / "metrics.csv").write_text("k,v\n", encoding="utf-8")
        paths = {f.path for f in run(repo, rs, None) if f.rule_id == "results-has-record"}
        if "results/paper_reproduction/20260601_120000" not in paths:
            failures.append("grouping-inner-record: まとめディレクトリ内の記録欠落を見逃しました")

        # まとめディレクトリの «中» は通常どおり検査すること (命名)
        (grp / "draft").mkdir()
        (grp / "draft" / "x.json").write_text("{}", encoding="utf-8")
        paths = {f.path for f in run(repo, rs, None) if f.rule_id == "results-dir-naming"}
        if "results/paper_reproduction/draft" not in paths:
            failures.append("grouping-inner-name: まとめディレクトリ内の非規約名を見逃しました")

    # 一次指標: 規約に準拠したリポジトリで 1 件も出さないこと (偽陽性ゼロ)
    clean_cases = [
        (_build_clean_repo, "replication-sim"),
        (_build_clean_rust_repo, "replication-rust"),
        (_build_clean_python_repo, "replication-python"),
    ]
    for builder, expected_id in clean_cases:
        with tempfile.TemporaryDirectory() as td:
            repo = builder(Path(td))
            rs = select_ruleset(repo, rulesets)
            if rs is None:
                failures.append(f"clean/{expected_id}: ルールセットが選択されませんでした")
                continue
            if rs.get("id") != expected_id:
                failures.append(
                    f"clean/{expected_id}: 誤ったルールセット '{rs.get('id')}' が選択されました"
                )
                continue
            found = run(repo, rs, None)
            if found:
                failures.append(
                    f"clean/{expected_id}: 偽陽性 "
                    + str([f"{f.rule_id}@{f.path}" for f in found])
                )

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        repo = _build_clean_repo(base)
        rs = select_ruleset(repo, rulesets)
        if rs is None:
            failures.append("clean: ルールセットが選択されませんでした")

        # 各ルールが実際に発火するか (壊したリポジトリで検出できること)
        cases = [
            ("missing-readme", lambda r: (r / "README.md").unlink(), "require-core-files"),
            (
                "bad-results-name",
                lambda r: (r / "results" / "output_2026").mkdir(),
                "results-dir-naming",
            ),
            (
                "no-config",
                lambda r: (r / "results" / "run_20260417_153000" / "config.json").unlink(),
                "results-has-record",
            ),
            (
                "gitignore-missing-results",
                lambda r: (r / ".gitignore").write_text(".claude/\n/target/\n", encoding="utf-8"),
                "gitignore-required-entries",
            ),
            (
                "name-drift",
                lambda r: (r / "tools" / "pyproject.toml").write_text(
                    '[project]\nname = "schelling-tools"\n', encoding="utf-8"
                ),
                "paper-key-consistency",
            ),
        ]
        for label, mutate, expected_rule in cases:
            with tempfile.TemporaryDirectory() as td2:
                repo2 = _build_clean_repo(Path(td2))
                mutate(repo2)
                rs2 = select_ruleset(repo2, rulesets)
                if rs2 is None:
                    failures.append(f"{label}: ルールセットが選択されませんでした")
                    continue
                ids = {f.rule_id for f in run(repo2, rs2, None)}
                if expected_rule not in ids:
                    failures.append(f"{label}: ルール {expected_rule} が発火しませんでした (検出: {ids})")

    if failures:
        print("selftest FAILED", file=sys.stderr)
        for f in failures:
            print("  - " + f, file=sys.stderr)
        return 1
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
