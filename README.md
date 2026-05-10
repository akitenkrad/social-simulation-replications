# Social Simulation Replications

社会科学系の古典的論文のシミュレーションを再現実装するプロジェクト集．
各実装は独立したリポジトリとしてGit Submoduleで管理しています．

## Replications

| 論文 | ディレクトリ | 言語 | 概要 |
|------|-------------|------|------|
| Schelling (1971) "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) | Rust + Python | エージェントベースの居住分離モデル．グリッド上のエージェントが近傍の同色比率に基づいて移動し，マクロな分離パターンが創発する過程を再現 |
| Axelrod (1997) "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) | Rust + Python | 文化拡散モデル．類似した文化ほど相互作用しやすく相互作用するとさらに類似するという局所的収斂メカニズムから，グローバルな文化的分極化が創発する過程を再現 |

## Simulators

汎用シミュレータコンポーネント．特定の論文の再現ではなく，再現実験や強化学習研究の基盤として横断的に使えるフレームワークを `simulators/` 配下に配置しています．

| 名称 | ディレクトリ | 言語 | 概要 |
|------|-------------|------|------|
| rs-othello-sim | [simulators/rs-othello-sim](https://github.com/akitenkrad/rs-othello-sim) | Rust + Python | オセロ ( Reversi) のシミュレーション・強化学習研究フレームワーク．Hybrid bitboard 盤面，棋譜 I/O ( JSON / GGF / WTHOR / JSONL)，TUI / CLI，Gymnasium / PettingZoo 互換 RL，PyO3 バインディング，外部エンジン連携 ( Edax / Egaroucid)，NN evaluator ( Candle)，PER replay buffer を含む |

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
