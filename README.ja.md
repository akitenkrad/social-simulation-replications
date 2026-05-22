<p align="center"><img src="docs/assets/hero.svg" width="100%"></p>

[English](README.md) | **日本語**

# Social Simulation Replications

社会科学系の古典的論文のシミュレーションを再現実装するプロジェクト集．各実装は独立したリポジトリとして Git Submodule で管理しています．

## Getting Started

```bash
# Submodule を含めてクローン
git clone --recurse-submodules git@github.com:akitenkrad/social-simulation-replications.git

# 既にクローン済みの場合は Submodule を取得
git submodule update --init --recursive
```

各実装の詳細な実行方法は，それぞれのディレクトリ内の README を参照してください．

## Documentation

- [Replications](docs/replications.ja.md) — 再現対象の論文カタログ（Schelling 1971, Axelrod 1997, Logistello）．
- [Simulators](docs/simulators.ja.md) — 汎用シミュレータコンポーネント．
- [Adding a Replication](docs/adding-a-replication.ja.md) — テンプレートから新規 Replication を作成する方法．

## License

MIT
