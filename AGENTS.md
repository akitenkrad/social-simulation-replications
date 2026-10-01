# AGENTS.md — social-simulation-replications

This monorepo collects independent **replications** of classic social-science
simulations and LLM-social studies, plus **original experiments** without a source paper.
Replications live under `replications/<paper_key>/` and experiments under
`experiments/<key>/`; each is its own git submodule with its own `README.md` /
`CLAUDE.md`. Most are built on the shared **socsim** platform in
`simulators/rs-social-simulation-tools/`.

## For AI agents

- **Building or extending a replication on socsim?** Read
  **[`simulators/rs-social-simulation-tools/AGENTS.md`](simulators/rs-social-simulation-tools/AGENTS.md)**
  first — it links the agent-oriented capability map and recipes for the library.
- **Working inside one replication or experiment?** Read that repository's own `README.md` and
  `.claude/CLAUDE.md` for its build/run/test commands and conventions.
- **Creating a run for development, debugging, or smoke testing?** Always pass
  `--scratch`; the run goes under `results/_scratch/` and is never synced. Clean
  up an accidental failed production run with `runvault delete`.
- `paper_key = {first-author surname}{year}` (lowercase ASCII) — the directory,
  submodule path, and workspace name all use it.
- Experiment `key` is a lowercase kebab-case theme name matching
  `^[a-z0-9]+(-[a-z0-9]+)*$` (for example, `dollar-auction-escalation`); the
  directory and submodule path use it.
- Rust/Python identifiers derive from one short lowercase `slug` (`<name>` in the
  template), separate from the catalog key: package `{slug}-simulation`, binary
  `{slug}`, Python package `{slug}-tools`, module `{slug_snake}_tools`
  (e.g. `schelling1971` → `schelling`, `hegselmann2002` → `hegselmann-bc` /
  `hegselmann_bc_tools`). Hyphens are allowed; when the slug has one, use the
  snake form for the module directory and the `[project.scripts]` target.
  `tools/review-kit` (`paper-key-consistency`) enforces this.
- To add an original experiment, follow
  [`docs/adding-an-experiment.md`](docs/adding-an-experiment.md).

See [`README.md`](README.md) for the project overview and the replication and experiment catalogs.
