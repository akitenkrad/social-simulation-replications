<p align="center"><img src="docs/assets/hero.svg" width="100%"></p>

**English** | [日本語](README.ja.md)

# Social Simulation Replications

A collection of replication implementations of classic social-science simulation papers. Each implementation lives in its own repository and is wired in here as a Git submodule.

## Replications

| Paper | Directory |
|-------|-----------|
| Schelling (1971), "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) |
| Axelrod (1997), "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) |
| Hegselmann & Krause (2005), "Opinion Dynamics Driven by Various Ways of Averaging" | [hegselmann2005](https://github.com/akitenkrad/hegselmann2005) |
| Granovetter (1973), "The Strength of Weak Ties" | [granovetter1973](https://github.com/akitenkrad/granovetter1973) |
| Chuang et al. (2024), "Simulating Opinion Dynamics with Networks of LLM-based Agents" | [chuang2024](https://github.com/akitenkrad/chuang2024) |
| Li et al. (2024), "EconAgent: LLM-Empowered Agents for Simulating Macroeconomic Activities" | [li2024](https://github.com/akitenkrad/li2024) |
| Gao et al. (2023), "S3: Social-network Simulation System with LLM-Empowered Agents" | [gao2023](https://github.com/akitenkrad/gao2023) |
| Ren et al. (2024), "Emergence of Social Norms in Generative Agent Societies (CRSEC)" | [ren2024](https://github.com/akitenkrad/ren2024) |
| Zhao et al. (2024), "CompeteAI: Understanding the Competition Dynamics of LLM-based Agents" | [zhao2024](https://github.com/akitenkrad/zhao2024) |
| Hua et al. (2024), "War and Peace (WarAgent): LLM-based Multi-Agent Simulation of World Wars" | [hua2024](https://github.com/akitenkrad/hua2024) |
| Yang et al. (2024), "OASIS: Open Agent Social Interaction Simulations with One Million Agents" | [yang2024](https://github.com/akitenkrad/yang2024) |
| Mou et al. (2024), "Unveiling the Truth and Facilitating Change: Towards Agent-based Large-scale Social Movement Simulation (HiSim)" | [mou2024](https://github.com/akitenkrad/mou2024) |
| Wang et al. (2025), "YuLan-OneSim: Towards the Next Generation of Social Simulator with Large Language Models" | [wang2025](https://github.com/akitenkrad/wang2025) |
| Han et al. (2023), "Guinea Pig Trials Utilizing GPT: A Smart Agent-Based Modeling Approach for Studying Firm Competition and Collusion (SABM)" | [han2023](https://github.com/akitenkrad/han2023) |
| Ji et al. (2024), "SRAP-Agent: Simulating and Optimizing Scarce Resource Allocation Policy with LLM-based Agent" | [ji2024](https://github.com/akitenkrad/ji2024) |
| Buro (1994–1999), "Logistello" (7 papers) | [logistello](https://github.com/akitenkrad/rs-logistello) |

## Simulators

General-purpose simulator components. These are not replications of any single paper; they sit under `simulators/` as cross-cutting frameworks that other replications and reinforcement-learning experiments can build on.

| Name | Directory |
|------|-----------|
| rs-social-simulation-tools | [simulators/rs-social-simulation-tools](https://github.com/akitenkrad/rs-social-simulation-tools) |
| rs-othello-sim | [simulators/rs-othello-sim](https://github.com/akitenkrad/rs-othello-sim) |

## Getting Started

```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:akitenkrad/social-simulation-replications.git

# Or fetch submodules after a regular clone
git submodule update --init --recursive
```

For run instructions, see the `README.md` inside each implementation directory.

## Documentation

- [Adding a Replication](docs/adding-a-replication.md) — how to scaffold a new replication from the template.

## License

MIT
