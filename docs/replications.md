**English** | [日本語](replications.ja.md)

# Replications

A collection of replication implementations of classic social-science simulation papers. Each implementation lives in its own repository and is wired in here as a Git submodule.

| Paper | Directory | Languages | Summary |
|-------|-----------|-----------|---------|
| Schelling (1971), "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) | Rust + Python | Agent-based residential-segregation model. Agents on a grid relocate based on the share of same-color neighbors, reproducing the emergence of macro-level segregation patterns from local preferences. |
| Axelrod (1997), "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) | Rust + Python | Cultural-dissemination model. Local convergence — culturally similar agents are more likely to interact and become even more similar — gives rise to global cultural polarization. |
| Buro (1994–1999), "Logistello" (7 papers) | [logistello](https://github.com/akitenkrad/rs-logistello) | Rust + Python | The world-champion-beating Othello program. Pattern-evaluation functions learned from expert games, ProbCut / Multi-ProbCut probabilistic forward pruning, and self-play opening-book learning — the methodological precursor to modern learned game AI. |

For run instructions, see the `README.md` inside each implementation directory.
