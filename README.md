[English](README.md) | [日本語](docs/ja/README.md)

# Social Simulation Replications

A collection of replication implementations of classic social-science simulation papers. Each implementation lives in its own repository and is wired in here as a Git submodule.

## Replications

| Paper | Directory | Languages | Summary |
|-------|-----------|-----------|---------|
| Schelling (1971), "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) | Rust + Python | Agent-based residential-segregation model. Agents on a grid relocate based on the share of same-color neighbors, reproducing the emergence of macro-level segregation patterns from local preferences. |
| Axelrod (1997), "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) | Rust + Python | Cultural-dissemination model. Local convergence — culturally similar agents are more likely to interact and become even more similar — gives rise to global cultural polarization. |
| Buro (1994–1999), "Logistello" (7 papers) | [logistello](https://github.com/akitenkrad/rs-logistello) | Rust + Python | The world-champion-beating Othello program. Pattern-evaluation functions learned from expert games, ProbCut / Multi-ProbCut probabilistic forward pruning, and self-play opening-book learning — the methodological precursor to modern learned game AI. |

## Simulators

General-purpose simulator components. These are not replications of any single paper; they sit under `simulators/` as cross-cutting frameworks that other replications and reinforcement-learning experiments can build on.

| Name | Directory | Languages | Summary |
|------|-----------|-----------|---------|
| rs-othello-sim | [simulators/rs-othello-sim](https://github.com/akitenkrad/rs-othello-sim) | Rust + Python | Othello (Reversi) simulation and reinforcement-learning research framework. Hybrid bitboard board, record I/O (JSON / GGF / WTHOR / JSONL), TUI / CLI, Gymnasium / PettingZoo-compatible RL, PyO3 bindings, external-engine integration (Edax / Egaroucid), NN evaluator (Candle), and PER replay buffer. |

## Getting Started

```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:akitenkrad/social-simulation-replications.git

# Or fetch submodules after a regular clone
git submodule update --init --recursive
```

For run instructions, see the `README.md` inside each implementation directory.

## License

MIT
