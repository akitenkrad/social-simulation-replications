[English](simulators.md) | **日本語**

# Simulators

汎用シミュレータコンポーネント．特定の論文の再現ではなく，再現実験や強化学習研究の基盤として横断的に使えるフレームワークを `simulators/` 配下に配置しています．

| 名称 | ディレクトリ | 言語 | 概要 |
|------|-------------|------|------|
| rs-othello-sim | [simulators/rs-othello-sim](https://github.com/akitenkrad/rs-othello-sim) | Rust + Python | オセロ ( Reversi) のシミュレーション・強化学習研究フレームワーク．Hybrid bitboard 盤面，棋譜 I/O ( JSON / GGF / WTHOR / JSONL)，TUI / CLI，Gymnasium / PettingZoo 互換 RL，PyO3 バインディング，外部エンジン連携 ( Edax / Egaroucid)，NN evaluator ( Candle)，PER replay buffer を含む |
| rs-social-simulation-tools | [simulators/rs-social-simulation-tools](https://github.com/akitenkrad/rs-social-simulation-tools) | Rust | コンポーザブルなエージェントベース社会シミュレーションプラットフォーム ( `socsim`)．実証研究の知見を，ニューラルネットのレイヤのように合成可能なメカニズムとして，6 フェーズ ( Environment → Decision → Interaction → Reward ＋ Pre/PostStep) の ABM + RL 風 tick ループに差し込める．決定論的なシード付き ChaCha20 RNG，ソーシャルネットワーク層 ( Erdős–Rényi / Watts–Strogatz / Barabási–Albert)，シナリオ TOML 駆動の CLI ( run / sweep / summarize，JSONL ログ)，較正済み HR ライフサイクル参照モジュール 9 メカニズム ( 採用・社会化・学習曲線・ピア効果・OCB・fit・離職・知識喪失・toxic 伝染) を含む |
