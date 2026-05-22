<p align="center"><img src="docs/assets/hero.svg" width="100%"></p>

**English** | [日本語](README.ja.md)

# Social Simulation Replications

A collection of replication implementations of classic social-science simulation papers. Each implementation lives in its own repository and is wired in here as a Git submodule.

## Getting Started

```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:akitenkrad/social-simulation-replications.git

# Or fetch submodules after a regular clone
git submodule update --init --recursive
```

For run instructions, see the `README.md` inside each implementation directory.

## Documentation

- [Replications](docs/replications.md) — the catalog of replicated papers (Schelling 1971, Axelrod 1997, Logistello).
- [Simulators](docs/simulators.md) — the general-purpose simulator components.
- [Adding a Replication](docs/adding-a-replication.md) — how to scaffold a new replication from the template.

## License

MIT
