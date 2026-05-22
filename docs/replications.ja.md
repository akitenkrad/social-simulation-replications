[English](replications.md) | **日本語**

# Replications

社会科学系の古典的論文のシミュレーションを再現実装するプロジェクト集．各実装は独立したリポジトリとして Git Submodule で管理しています．

| 論文 | ディレクトリ | 言語 | 概要 |
|------|-------------|------|------|
| Schelling (1971) "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) | Rust + Python | エージェントベースの居住分離モデル．グリッド上のエージェントが近傍の同色比率に基づいて移動し，マクロな分離パターンが創発する過程を再現 |
| Axelrod (1997) "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) | Rust + Python | 文化拡散モデル．類似した文化ほど相互作用しやすく相互作用するとさらに類似するという局所的収斂メカニズムから，グローバルな文化的分極化が創発する過程を再現 |
| Buro (1994–1999) "Logistello"（7論文） | [logistello](https://github.com/akitenkrad/rs-logistello) | Rust + Python | 世界チャンピオンを破った Othello プログラム．専門家棋譜から学習するパターン評価関数，ProbCut / Multi-ProbCut 確率的前向き枝刈り，自己対戦による定石学習を統合．現代の学習型ゲーム AI の方法論的祖型 |

各実装の詳細な実行方法は，それぞれのディレクトリ内の README を参照してください．
