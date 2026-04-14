# Social Simulation Replications

社会科学系の古典的論文のシミュレーションを再現実装するプロジェクト集．
各実装は独立したリポジトリとしてGit Submoduleで管理しています．

## Replications

| 論文 | ディレクトリ | 言語 | 概要 |
|------|-------------|------|------|
| Schelling (1971) "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) | Rust + Python | エージェントベースの居住分離モデル．グリッド上のエージェントが近傍の同色比率に基づいて移動し，マクロな分離パターンが創発する過程を再現 |
| Axelrod (1997) "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) | Rust + Python | 文化拡散モデル．類似した文化ほど相互作用しやすく相互作用するとさらに類似するという局所的収斂メカニズムから，グローバルな文化的分極化が創発する過程を再現 |

## Getting Started

```bash
# Submoduleを含めてクローン
git clone --recurse-submodules git@github.com:akitenkrad/social-simulation-replications.git

# 既にクローン済みの場合はSubmoduleを取得
git submodule update --init --recursive
```

各実装の詳細な実行方法は，それぞれのディレクトリ内のREADMEを参照してください．

## License

MIT
