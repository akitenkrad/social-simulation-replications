<p align="center"><img src="docs/assets/hero.svg" width="100%"></p>

[English](README.md) | **日本語**

# Social Simulation Replications

社会科学系の古典的論文のシミュレーションを再現実装するプロジェクト集．各実装は独立したリポジトリとして Git Submodule で管理しています．

## Replications

| 論文 | ディレクトリ |
|------|-------------|
| Schelling (1971) "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) |
| Axelrod (1997) "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) |
| Hegselmann & Krause (2005) "Opinion Dynamics Driven by Various Ways of Averaging" | [hegselmann2005](https://github.com/akitenkrad/hegselmann2005) |
| Granovetter (1973) "The Strength of Weak Ties" | [granovetter1973](https://github.com/akitenkrad/granovetter1973) |
| Chuang et al. (2024) "Simulating Opinion Dynamics with Networks of LLM-based Agents" | [chuang2024](https://github.com/akitenkrad/chuang2024) |
| Li et al. (2024) "EconAgent: LLM-Empowered Agents for Simulating Macroeconomic Activities" | [li2024](https://github.com/akitenkrad/li2024) |
| Gao et al. (2023) "S3: Social-network Simulation System with LLM-Empowered Agents" | [gao2023](https://github.com/akitenkrad/gao2023) |
| Ren et al. (2024) "Emergence of Social Norms in Generative Agent Societies (CRSEC)" | [ren2024](https://github.com/akitenkrad/ren2024) |
| Zhao et al. (2024) "CompeteAI: Understanding the Competition Dynamics of LLM-based Agents" | [zhao2024](https://github.com/akitenkrad/zhao2024) |
| Hua et al. (2024) "War and Peace (WarAgent): LLM-based Multi-Agent Simulation of World Wars" | [hua2024](https://github.com/akitenkrad/hua2024) |
| Yang et al. (2024) "OASIS: Open Agent Social Interaction Simulations with One Million Agents" | [yang2024](https://github.com/akitenkrad/yang2024) |
| Mou et al. (2024) "Unveiling the Truth and Facilitating Change: Towards Agent-based Large-scale Social Movement Simulation (HiSim)" | [mou2024](https://github.com/akitenkrad/mou2024) |
| Buro (1994–1999) "Logistello"（7論文） | [logistello](https://github.com/akitenkrad/rs-logistello) |

## Simulators

汎用シミュレータコンポーネント．特定の論文の再現ではなく，再現実験や強化学習研究の基盤として横断的に使えるフレームワークを `simulators/` 配下に配置しています．

| 名称 | ディレクトリ |
|------|-------------|
| rs-social-simulation-tools | [simulators/rs-social-simulation-tools](https://github.com/akitenkrad/rs-social-simulation-tools) |
| rs-othello-sim | [simulators/rs-othello-sim](https://github.com/akitenkrad/rs-othello-sim) |

## Getting Started

```bash
# Submodule を含めてクローン
git clone --recurse-submodules git@github.com:akitenkrad/social-simulation-replications.git

# 既にクローン済みの場合は Submodule を取得
git submodule update --init --recursive
```

各実装の詳細な実行方法は，それぞれのディレクトリ内の README を参照してください．

## Documentation

- [Adding a Replication](docs/adding-a-replication.ja.md) — テンプレートから新規 Replication を作成する方法．

## License

MIT
