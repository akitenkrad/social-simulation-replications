[English](adding-an-experiment.md) | **日本語**

# Experiment の追加方法

共通テンプレートは，出典論文を持たない独自の社会シミュレーション実験にも使用できる．Replication と同じく，Cargo workspace + uv workspace の 2 プロジェクト構成（Rust シミュレーション + Python ツール）の雛形を提供する．

## 構成

```
template/
├── README.md                      ← 共通テンプレートの使い方
└── files/                         ← コピー対象本体
    ├── Cargo.toml                 (workspace ルート)
    ├── pyproject.toml             (uv workspace ルート)
    ├── README.md                  (placeholder 入り)
    ├── .gitignore
    ├── _claude/CLAUDE.md          ← .claude/ にリネームしてコピー（placeholder 入り）
    ├── simulation/                ← Rust プロジェクト
    │   ├── Cargo.toml
    │   └── src/main.rs
    └── tools/                     ← Python プロジェクト（src レイアウト）
        ├── pyproject.toml
        └── src/_NAME_tools/       ← {NAME}_tools にリネーム必要
```

## 命名規則

Experiment は 2 つの識別子を持つ．両者は別の値であり，取り違えないこと．

| 識別子 | 規則 | 例 | 用途 |
|--------|------|----|------|
| key（`<key>`） | `exp-{subject}-{change}`．小文字 kebab-case で，プレフィックスの後ろは 2〜4 語 | `exp-dollar-auction-escalation` | ディレクトリ名，Submodule のパス，GitHub リポジトリ名，runvault の `repo_id`，`replications.toml` の `key` / `repo` |
| slug（`<name>`） | 短い小文字の名前．`exp-` プレフィックスは**付けない** | `dollar-auction` | Rust の crate・バイナリ，Python パッケージの名前（プレースホルダ `{{NAME}}`） |

- *subject* は回すゲームやモデル（`dollar-auction`，`rumor`），*change* は教科書的な設定から変えた点（`escalation`，`forgetting`）である．
- key は `^exp-[a-z0-9]+(-[a-z0-9]+)*$` に一致する．`replications.toml` の `repo` は `key` と同じ文字列にする．
- この規則より前からある 5 本の実験は `exp-<旧 key>` に改名し，それ以外はそのまま残した．そのため，すべてが subject–change の形に読めるわけではない．
- key は runvault の `repo_id` でもあり，runvault-socsim は実験固有のイベント種別を `x.<repo_id>.<kind>` という名前空間に置く．そのためリポジトリを改名するとイベント種別も変わる．run の出力を読む側はイベント種別をハードコードしないこと．

slug はハイフンを含んでよいが，アンダースコアは不可（例 `dollar-auction`）．`<name_snake>` はハイフンをアンダースコアに置き換えた同じ値（`dollar_auction`）で，Python のモジュールディレクトリと `[project.scripts]` の参照先にだけ使う．すべての派生名が 1 つの slug から導かれていることは `tools/review-kit` が検査する．

## 使い方（手動セットアップ）

```bash
# 親リポジトリのルートで実行する想定

# 1. テンプレートをコピー
mkdir -p experiments
cp -R template/files experiments/<key>

# 2. プレースホルダ {{NAME}} を <name> に一括置換
#    macOS の sed は -i '' 形式が必要．Linux は -i だけで可
find experiments/<key> -type f -exec sed -i '' \
  -e 's/{{NAME}}_tools/<name_snake>_tools/g' -e 's/{{NAME}}/<name>/g' {} \;

# 3. Python パッケージディレクトリをリネーム
mv experiments/<key>/tools/src/_NAME_tools \
   experiments/<key>/tools/src/<name_snake>_tools

# 4. _claude/ を .claude/ にリネーム（親リポジトリの .gitignore 回避用の仮名）
mv experiments/<key>/_claude experiments/<key>/.claude

# 5. ビルド・依存解決を確認
cd experiments/<key>
cargo build --release
uv sync
uv run <name>-tools --help
```

### 6. Experiment リポジトリを初期化して最初のコミットを作成

```bash
# experiments/<key> 内で引き続き実行
git init
git add .
git commit -m "Initial experiment implementation"
```

### 7. GitHub リポジトリを作成して push

用途に応じて `--public` または `--private` を選び，`akitenkrad/<key>` を作成して最初のコミットを push する：

```bash
gh repo create akitenkrad/<key> --public --source . --push
# 非公開にする場合は --public を --private に置き換える．
```

GitHub 側で先にリポジトリを作成し，`origin` を追加して現在のブランチを push してもよい．

### 8. 親リポジトリへ Submodule として登録

```bash
cd ../..
git submodule add git@github.com:akitenkrad/<key>.git experiments/<key>
```

`git submodule add` は追加先に既存の Git リポジトリがあっても受け付けるため，作成してコミットしたディレクトリを削除したり，再 clone したりする必要はない．

### 9. カタログへ登録

`replications.toml` に 6 個の必須フィールドを追加する：

```toml
[[experiment]]
key = "exp-dollar-auction-escalation"
repo = "exp-dollar-auction-escalation"
year = 2026
title = "LLM-Agent Escalation in the Dollar Auction"
theme_en = "Escalation and sunk-cost behavior"
theme_ja = "エスカレーションと埋没費用行動"
```

その後，全カタログ対象を再生成して確認する：

```bash
python3 tools/gen_catalog.py
python3 tools/gen_catalog.py --check
```

### 10. 親モノレポの変更をコミット

```bash
git add .gitmodules experiments/<key> replications.toml \
  README.md README.ja.md docs/experiments.md docs/experiments.ja.md
git commit -m "Add <key> experiment"
```

### 例: ドル・オークションのエスカレーション

key は `exp-dollar-auction-escalation`，slug は `dollar-auction`（snake 形は `dollar_auction`）：

```bash
cp -R template/files experiments/exp-dollar-auction-escalation
find experiments/exp-dollar-auction-escalation -type f -exec sed -i '' \
  -e 's/{{NAME}}_tools/dollar_auction_tools/g' -e 's/{{NAME}}/dollar-auction/g' {} \;
mv experiments/exp-dollar-auction-escalation/tools/src/_NAME_tools \
   experiments/exp-dollar-auction-escalation/tools/src/dollar_auction_tools
mv experiments/exp-dollar-auction-escalation/_claude experiments/exp-dollar-auction-escalation/.claude
```

その後，リポジトリを `akitenkrad/exp-dollar-auction-escalation` として作成し，
`git submodule add git@github.com:akitenkrad/exp-dollar-auction-escalation.git experiments/exp-dollar-auction-escalation` で追加する．

## Run の記録

runvault 連携はテンプレートに含まれない．`replications/rep-schelling1971/` の `runvault.toml`，Rust の `runvault` 依存関係，Python の `runvault[read]` 依存関係を参照して追加する．開発，デバッグ，スモークテストの実行では常に `--scratch` を渡す．scratch run は `results/_scratch/` に保存され，同期されない．

## 留意点

- `{{NAME}}` が未置換のテンプレート状態では単独実行できない．
- 雛形の作成後に，プロジェクト固有のシミュレーションロジックと分析コマンドを実装する．
- `_claude/` は親リポジトリの `.gitignore` を回避するための仮名である．コピー後は必ず `.claude/` にリネームする．
- 共通雛形と runvault 連携の完成例は `replications/rep-schelling1971/` を参照する．
