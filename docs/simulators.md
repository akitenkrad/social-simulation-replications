**English** | [日本語](simulators.ja.md)

# Simulators

General-purpose simulator components. These are not replications of any single paper; they sit under `simulators/` as cross-cutting frameworks that other replications and reinforcement-learning experiments can build on.

| Name | Directory | Languages | Summary |
|------|-----------|-----------|---------|
| rs-othello-sim | [simulators/rs-othello-sim](https://github.com/akitenkrad/rs-othello-sim) | Rust + Python | Othello (Reversi) simulation and reinforcement-learning research framework. Hybrid bitboard board, record I/O (JSON / GGF / WTHOR / JSONL), TUI / CLI, Gymnasium / PettingZoo-compatible RL, PyO3 bindings, external-engine integration (Edax / Egaroucid), NN evaluator (Candle), and PER replay buffer. |
| rs-social-simulation-tools | [simulators/rs-social-simulation-tools](https://github.com/akitenkrad/rs-social-simulation-tools) | Rust | Composable agent-based social-simulation platform (`socsim`). Empirical research findings plug in as composable mechanisms — like neural-net layers — over a 6-phase (Environment → Decision → Interaction → Reward, plus Pre/PostStep) ABM + RL-style tick loop. Deterministic seeded ChaCha20 RNG, social-network layer (Erdős–Rényi / Watts–Strogatz / Barabási–Albert), scenario-TOML CLI (run / sweep / summarize, JSONL logs), and a calibrated HR-lifecycle reference module of nine mechanisms (hiring, socialization, learning curve, peer effect, OCB, fit, turnover, knowledge loss, toxic spread). |
