# Simulation Project Template

> 親リポジトリ向けの解説は [docs/adding-a-replication.ja.md](../docs/adding-a-replication.ja.md) と [docs/adding-an-experiment.ja.md](../docs/adding-an-experiment.ja.md) を参照．

社会シミュレーションの論文再現と独自実験に共通するプロジェクトテンプレート．Cargo workspace + uv workspace の 2 プロジェクト構成（Rust シミュレーション + Python ツール）の雛形を提供する．

## 構成

```
template/
├── README.md                      ← このファイル（テンプレートの使い方）
└── files/                         ← コピー対象本体
    ├── Cargo.toml                 (workspace ルート)
    ├── pyproject.toml             (uv workspace ルート)
    ├── README.md                  (placeholder 入り)
    ├── .gitignore
    ├── _claude/CLAUDE.md          ← .claude/ にリネームしてコピー（placeholder 入り）
    ├── simulation/                ← Rust プロジェクト
    │   ├── Cargo.toml
    │   └── src/main.rs
    └── tools/                     ← Python プロジェクト (src レイアウト)
        ├── pyproject.toml
        └── src/_NAME_tools/       ← {NAME}_tools にリネーム必要
            ├── __init__.py
            ├── cli.py
            ├── visualize.py
            ├── visualize_sweep.py             ← スイープ可視化 + 組み合わせ別グリッドアニメーション
            └── show_experiment_settings.py  ← 実行結果の config.json 表示
```

## プレースホルダ

| Placeholder | 意味 | 例 |
|-------------|------|---|
| `{{NAME}}` | slug．key の `rep-` / `exp-` を付けないパッケージプレフィックス（小文字英字推奨） | `axelrod`, `schelling` |

`{{NAME}}` 1 つから以下の識別子が派生する：

- Rust crate: `<NAME>-simulation`
- Rust binary: `<NAME>`
- Python package: `<NAME_snake>_tools` （ディレクトリ名・モジュール名．`<NAME>` のハイフンはアンダースコアに置き換える）
- Python CLI: `<NAME>-tools`

## 使い方（手動セットアップ）

新規プロジェクトを `replications/<key>/` または `experiments/<key>/` 以下に作成する手順．`<key>` はディレクトリ名・Submodule のパス・GitHub リポジトリ名・runvault の `repo_id` を兼ねる識別子で，Replication は `rep-{筆頭著者の姓}{年}`（例: `rep-axelrod1997`），Experiment は `exp-{subject}-{change}`（例: `exp-dollar-auction-escalation`）とする．`<name>` は key とは別の slug で，プレフィックスを付けない（例: `axelrod`，`dollar-auction`．ハイフンを含む場合の Python モジュール名 `<name_snake>` はアンダースコア形）．規則の詳細は [docs/adding-a-replication.ja.md](../docs/adding-a-replication.ja.md#命名規則) と [docs/adding-an-experiment.ja.md](../docs/adding-an-experiment.ja.md#命名規則) を参照．以下は Replication の例であり，Experiment では対象パスを `experiments/<key>` に置き換える．

```bash
# 親リポジトリのルートで実行する想定

# 1. テンプレートをコピー
cp -R template/files replications/<key>

# 2. プレースホルダ {{NAME}} を <name> に一括置換
#    (macOS の sed は -i '' 形式が必要．Linux は -i だけで可)
find replications/<key> -type f -exec sed -i '' \
  -e 's/{{NAME}}_tools/<name_snake>_tools/g' -e 's/{{NAME}}/<name>/g' {} \;

# 3. Python パッケージディレクトリをリネーム
mv replications/<key>/tools/src/_NAME_tools \
   replications/<key>/tools/src/<name_snake>_tools

# 4. _claude/ を .claude/ にリネーム（親リポジトリの .gitignore 回避用の仮名）
mv replications/<key>/_claude replications/<key>/.claude

# 5. ビルド・依存解決を確認
cd replications/<key>
cargo build --release
uv sync
uv run <name>-tools --help
```

### 例: Axelrod (1997)

key は `rep-axelrod1997`，slug は `axelrod`：

```bash
cp -R template/files replications/rep-axelrod1997
find replications/rep-axelrod1997 -type f -exec sed -i '' 's/{{NAME}}/axelrod/g' {} \;
mv replications/rep-axelrod1997/tools/src/_NAME_tools \
   replications/rep-axelrod1997/tools/src/axelrod_tools
mv replications/rep-axelrod1997/_claude replications/rep-axelrod1997/.claude

cd replications/rep-axelrod1997
cargo build --release
uv sync
uv run axelrod-tools --help
```

## 留意点

- テンプレート状態のファイル（`{{NAME}}` 未置換）は単独で実行できない．特に Python の import 文に placeholder が含まれるため，置換前は構文上有効でもランタイムエラーになる．
- `simulation/src/main.rs` には clap の `run` / `sweep` サブコマンド分岐の最小骨格だけが含まれる．シミュレーションロジックは各プロジェクトで実装する．`run` は `<output_dir>/config.json`，`sweep` は `<output_dir>/sweep_config.json` を必ず書き出すこと（`show-experiment-settings` が読む）．`sweep` 側に `--snapshot-interval N` (N>0) で各 run の `snapshots/step_*.csv` を出力する経路を用意しておくこと（`visualize-sweep` の組み合わせ別グリッドアニメーションが必要とする）．
- `tools/src/<name>_tools/cli.py` は `visualize` / `visualize-sweep` / `show-experiment-settings` サブコマンドへのディスパッチ骨格．プロジェクト固有のサブコマンドは必要に応じて追加する．
- `visualize_sweep.py` は CLI 骨格と設計指針コメントだけを持つ TODO ファイル．パラメータ依存図と組み合わせ別グリッドアニメーション (`sweep_grid_animation.gif`) の実装は各プロジェクトで埋める（参考実装: `replications/rep-schelling1971/`）．
- `show_experiment_settings.py` は汎用の `--results-dir` モードのみを持つ．Replication で論文再現実験定義の一覧表示が必要な場合に限り，`reproduce_paper.py` を作成し，そこから `Experiment` / `paper_experiments()` をインポートして拡張する（`replications/rep-schelling1971/` 参照）．
- `_claude/` は親リポジトリの `.gitignore`（`.claude/` 全体を除外）を回避するための仮名．コピー後は必ず `.claude/` にリネームすること．
- 共通構成のリファレンス実装は `replications/rep-schelling1971/` を参照．
