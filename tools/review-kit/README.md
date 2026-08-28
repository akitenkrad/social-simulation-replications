# review-kit

再現実装リポジトリの**規約準拠チェッカ**．`replications/` 配下の各リポジトリに対し，ディレクトリ構成・命名・出力形式の構造的制約だけを決定的に検証する．

本体は `social-simulation-replications/tools/review-kit/` に置く．標準ライブラリのみに依存し，`scripts/` と `rules/` が隣り合っていればどこからでも動く．

`CHECK=tools/review-kit/scripts/check_conventions.py` として，親リポジトリのルートから:

```bash
# 25 リポジトリを一括走査 + 集約表
python3 $CHECK --root replications --each

# 内蔵フィクスチャで自己検査 (ルールに手を入れたら必ず通す)
python3 $CHECK --selftest
```

個別の再現実装リポジトリの中からは，絶対パスで呼ぶ:

```bash
CHECK=~/Documents/workspace/social-simulation-replications/tools/review-kit/scripts/check_conventions.py

# カレントから .git を探索して 1 リポジトリだけ検査
python3 $CHECK

# フック用 (変更パスに関係するルールだけ実行)
python3 $CHECK --changed simulation/src/main.rs
```

`--block` を付けたときだけ high の指摘で exit 2．既定は非ブロッキング (exit 0)．

---

## 規約の単一真実源

**`rules/*.json` が唯一の真実源である．**

| | 役割 |
|---|---|
| `review-kit/rules/*.json` | **強制される規約**の真実源．「実装が必ず満たさねばならない性質」だけを書く |
| `my-skills/skills/{socsim-,}replication-design/` | 設計書の**生成ガイド**．既定値・推奨形・テンプレートを書く．必須要件は書かない |

生成スキル側の記述は，特記が無い限り「既定値 (推奨)」であって要件ではない．両者が食い違ったらルールセットが正しい．

### ルールを変える手順

1. `rules/*.json` を変更する
2. `--selftest` に **2 種類**のケースを追加する — (a) 規約準拠のリポジトリで発火しないこと，(b) 破ったら発火すること．**(a) が一次指標**である
3. `--selftest` を通す
4. 25 リポジトリへ `--each` で再走査し，集約表の発火分布を見る
5. 対応する SKILL.md / references を，新しいルールに合わせて更新する

**逆方向 (SKILL.md を先に変えてルールを後追いさせる) はしない．** ルールセットには実態の突き合わせ結果が入っており，SKILL.md には入っていない．

各ルールセットの `source` フィールドは，対応する生成スキルを指す (同期先の目印であって，真実源ではない)．

> [!NOTE] 集約表の読み方
> **「全リポジトリで発火」しているルールは，中身が正しく見えてもルール側が間違っている強い証拠**として扱う．初回走査の 436 件のうち約 89% がこれだった．

---

## 設計上の教訓 — 意味の判定を決定的なチェックに押し込まない

convention 軸は「曖昧さのない構造的検査」だけを持つ．**「良い実装か」「意図が満たされているか」の判断は持たない．** この境界を 3 回破り，そのたびに大量の誤検出を出した．

| # | 押し込もうとした判定 | 症状 | 決定的な形に落とし直した結果 |
|---|---|---|---|
| 1 | 内部識別子が「著者姓+年」という**意味のある形**か | 25/25 で発火．実際の識別子は論文のシステム名 (`oasis`, `econagent`, `waragent`) や著者-トピック (`brinsfield-silence`) で，どれも妥当だった | **形は問わない．** 派生名 (package / bin / tools / module) が 1 つの識別子から一貫して導かれているかだけを見る (`paper-key-consistency`) |
| 2 | 結果ディレクトリが `{サブコマンド}_{タイムスタンプ}` **という並び**か | 接頭形・接尾形・タイムスタンプのみが併存し，どれも実害が無かった | **並びは問わない．** 名前にタイムスタンプを含むかだけを見る (含まないと再実行で上書きされる，という実害に対応) (`results-dir-naming`) |
| 3 | 実験条件が `config.json` に**十分に記録**されているか | `reproduce_summary.json` の `config` ブロック，`cargo_invocations` + `run_dirs`，トップレベルのフラットなパラメータ — いずれも十分な記録なのに発火した | **十分性は判定しない．** 「JSON が 1 つも無い」ことだけを見る (`results-has-record`)．記録が復元に足りるかの判断は repro 軸 (LLM スキル) が担当する |

共通する失敗の形は，**「守らせたい意図」をそのまま検査条件に翻訳したこと**である．意図は多くの正しい実装形を許すが，決定的なチェックは 1 つの形しか許せない．差分がそのまま誤検出になる．

書くべきなのは意図ではなく，**意図が破られたときに必ず観測される最小の構造的性質**である (3 なら「復元できるか」ではなく「機械可読な記録がゼロか」)．曖昧さが残るなら，それは convention 軸の担当ではない．

> ルールを 1 つ足すたびに問うこと: **「このルールが発火しないが実装として不適切」という例と，「発火するが実装として妥当」という例を挙げられるか．** 後者が挙がるなら，そのルールは意味の判定を含んでいる．

### 軸の分担

| 軸 | 担当 | 実装 |
|---|---|---|
| **convention** | 曖昧さのない構造的検査 | `scripts/check_conventions.py` (本リポジトリ) |
| **repro** | 記録が実行条件の復元に足りるかの判断 | 未実装 (LLM スキル) |
| **yagni** / **api** | — | 未実装 |

repro 軸の評価フィクスチャになる実例 (走査で判明済み):

- 陽性 (十分な記録): `hegselmann2005` の `cargo_invocations` + `run_dirs`，`granovetter1973` のフラットなパラメータ，`yang2024` の `config` ブロック
- 陰性 (不十分): `noelleneumann1974` の anchors のみ (JSON はあるが条件が無い — convention 軸では意図的に見逃している)，`jones2022` の CSV のみ

---

## ルールセット

| ファイル | 対象 | 判定条件 |
|---|---|---|
| `rules/replication-sim.json` | Rust + Python モノレポ (socsim) | `simulation/Cargo.toml` と `tools/pyproject.toml` の両方 |
| `rules/replication-rust.json` | Rust 単体 | — |
| `rules/replication-python.json` | Python 単体 | — |

主要ルール:

| ルール | severity | 検査内容 |
|---|---|---|
| `require-core-files` | medium | `README.md` / `.gitignore` / `.claude/CLAUDE.md` 等の存在 |
| `gitignore-required-entries` | high | `.claude/` `results/` `target/` が `.gitignore` にあること．**表記は正規化して比較する** (`/target/` と `target/` と `target` は同一とみなす) |
| `local-only-not-tracked` | high | `.claude/` と `results/` が追跡されていないこと |
| `results-dir-naming` | medium | `results/` の子ディレクトリ名がタイムスタンプ `YYYYMMDD_HHMMSS` を含むこと (並びは自由) |
| `results-has-record` | medium | `results/<dir>/` に JSON が 1 つ以上あること (内容は見ない) |
| `paper-key-consistency` / `package-name-consistency` | medium | package / bin / tools / module 名が 1 つの識別子から導かれていること (識別子の形は問わない) |

`latest` シンボリックリンクは `results/` 配下の検査から除外される．

---

## 現状と残課題

25 リポジトリ走査時点で **指摘 1 件**．内訳の推移は次のとおり．

| 時点 | 指摘 | 内容 |
|---|---|---|
| 初回走査 | 436 件 | うち約 89% はルール側の誤り．規約が実態と乖離していた |
| ルール修正後 | 49 件 | high ゼロ / 13 リポジトリがクリーン．残りは 3 つの構造的課題の症状だった |
| 構造的課題の解消後 | 1 件 | 下記 3 課題に対応した結果 |

| 課題 | 状態 |
|---|---|
| 1. 規約の単一真実源化 | 対応済み．真実源は `rules/*.json`．`socsim-replication-design` / `replication-design` の両 SKILL.md を性質ベースに改訂し，真実源への参照を入れた |
| 2. テンプレート展開の決定的化 | 対応済み．根本原因はテンプレート展開の非決定性ではなく，旧 `socsim-replication-design/SKILL.md` が `paper_key` (ディレクトリ用) と短縮 `crate_slug` (crate 用) の **2 レベル命名を明示的に指示していた**こと．規約を単一 `slug` に改訂し，11 リポジトリの識別子を統一した |
| 3. reproduce の実行記録欠落 | 対応済み．`socsim-reproduce` は CSV ライタ 2 本しか持たず **JSON レコードの API を提供していない**ため，これを呼ぶだけで済ませた 4 実装が揃って条件を落としていた．各呼び出し側で条件 JSON を書くよう修正し，実行して確認済み |

残る 1 件は `schelling1971/results/paper_reproduction/20260717_111500`．
`reproduce_paper.py` の出力ではなく (同ディレクトリに `regen_bnm_groups.py` が同梱されている)，
図だけを手作業で再生成した際に作られたディレクトリで，実行記録が無い．削除するか記録を足すかは要判断．

### 恒久策として残っている提案

`socsim-reproduce` に «`paper_anchors.csv` + `reproduce_summary.csv` + 条件 JSON» を一括で書く
バンドル API を足すと，将来の再現実装が JSON を落とせなくなる．
ただし replications は `branch = "main"` の git 依存で socsim を参照しているため，
反映には `rs-social-simulation-tools` への push と各リポジトリでの `cargo update` が要る．

---
*This file was generated by Claude Code.*
