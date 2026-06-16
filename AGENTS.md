# AGENTS.md — social-simulation-replications

This monorepo collects independent **replications** of classic social-science
simulations and LLM-social studies. Each replication lives under `replications/<paper_key>/`
(its own git submodule, with its own `README.md` / `CLAUDE.md`), and most are
built on the shared **socsim** platform in `simulators/rs-social-simulation-tools/`.

## For AI agents

- **Building or extending a replication on socsim?** Read
  **[`simulators/rs-social-simulation-tools/AGENTS.md`](simulators/rs-social-simulation-tools/AGENTS.md)**
  first — it links the agent-oriented capability map and recipes for the library.
- **Working inside one replication?** Read that replication's own `README.md` and
  `.claude/CLAUDE.md` for its build/run/test commands and conventions.
- `paper_key = {first-author surname}{year}` (lowercase ASCII) — the directory,
  submodule path, and workspace name all use it.

See [`README.md`](README.md) for the project overview and the list of replications.
