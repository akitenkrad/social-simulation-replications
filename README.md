<p align="center"><img src="docs/assets/hero.svg" width="100%"></p>

**English** | [日本語](README.ja.md)

# Social Simulation Replications

A collection of replication implementations of classic social-science simulation papers. Each implementation lives in its own repository and is wired in here as a Git submodule.

## Replications

| Paper | Directory |
|-------|-----------|
| Schelling (1971), "Dynamic Models of Segregation" | [schelling1971](https://github.com/akitenkrad/schelling1971) |
| Axelrod (1997), "The Dissemination of Culture" | [axelrod1997](https://github.com/akitenkrad/axelrod1997) |
| Buro (1994–1999), "Logistello" (7 papers) | [logistello](https://github.com/akitenkrad/rs-logistello) |

## Simulators

General-purpose simulator components. These are not replications of any single paper; they sit under `simulators/` as cross-cutting frameworks that other replications and reinforcement-learning experiments can build on.

| Name | Directory |
|------|-----------|
| rs-othello-sim | [simulators/rs-othello-sim](https://github.com/akitenkrad/rs-othello-sim) |
| rs-social-simulation-tools | [simulators/rs-social-simulation-tools](https://github.com/akitenkrad/rs-social-simulation-tools) |

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
