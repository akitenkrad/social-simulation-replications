**English** | [日本語](adding-a-replication.ja.md)

# Adding a Replication

A template for new replication implementations of classic social-science papers. It provides a scaffold for the two-project layout (Cargo workspace + uv workspace — a Rust simulation plus Python tooling).

## Layout

```
template/
├── README.md                      ← guide on how to use the template
└── files/                         ← the payload that gets copied
    ├── Cargo.toml                 (workspace root)
    ├── pyproject.toml             (uv workspace root)
    ├── README.md                  (with placeholders)
    ├── .gitignore
    ├── _claude/CLAUDE.md          ← rename to .claude/ when copying (with placeholders)
    ├── simulation/                ← Rust project
    │   ├── Cargo.toml
    │   └── src/main.rs
    └── tools/                     ← Python project (src layout)
        ├── pyproject.toml
        └── src/_NAME_tools/       ← must be renamed to {NAME}_tools
            ├── __init__.py
            ├── cli.py
            ├── visualize.py
            ├── visualize_sweep.py             ← sweep visualization + per-combination grid animation
            └── show_experiment_settings.py  ← display the config.json of a run
```

## Placeholder

| Placeholder | Meaning | Example |
|-------------|---------|---------|
| `{{NAME}}` | Package prefix (lowercase letters recommended) | `axelrod`, `schelling` |

A single `{{NAME}}` derives the following identifiers:

- Rust crate: `<NAME>-simulation`
- Rust binary: `<NAME>`
- Python package: `<NAME>_tools` (directory name / module name)
- Python CLI: `<NAME>-tools`

## Usage (manual setup)

Steps to create a new project under `replications/<paper_key>/`. `<paper_key>` is the paper identifier (e.g. `axelrod1997`), and `<name>` is the package prefix (e.g. `axelrod`).

```bash
# Intended to be run from the parent repository root

# 1. Copy the template
cp -R template/files replications/<paper_key>

# 2. Replace the {{NAME}} placeholder with <name> everywhere
#    (macOS sed needs the -i '' form; on Linux -i alone is fine)
find replications/<paper_key> -type f -exec sed -i '' 's/{{NAME}}/<name>/g' {} \;

# 3. Rename the Python package directory
mv replications/<paper_key>/tools/src/_NAME_tools \
   replications/<paper_key>/tools/src/<name>_tools

# 4. Rename _claude/ to .claude/ (the placeholder name dodges the parent repo's .gitignore)
mv replications/<paper_key>/_claude replications/<paper_key>/.claude

# 5. Verify the build and dependency resolution
cd replications/<paper_key>
cargo build --release
uv sync
uv run <name>-tools --help
```

### 6. Register the replication in the catalog

The replication tables in `README.md`, `README.ja.md`, and `docs/replications*.md` are auto-generated from `replications.toml` at the repo root. Do **not** edit those tables by hand. Instead:

```bash
# Append a [[replication]] entry to replications.toml (see existing entries for the
# field list: key, repo, author, year, year_display?, title, paradigm, domain, theme_en, theme_ja)
# then regenerate every catalog target:
python3 tools/gen_catalog.py

# Verify nothing is stale (useful in CI):
python3 tools/gen_catalog.py --check
```

### Example: Axelrod (1997)

```bash
cp -R template/files replications/axelrod1997
find replications/axelrod1997 -type f -exec sed -i '' 's/{{NAME}}/axelrod/g' {} \;
mv replications/axelrod1997/tools/src/_NAME_tools \
   replications/axelrod1997/tools/src/axelrod_tools
mv replications/axelrod1997/_claude replications/axelrod1997/.claude

cd replications/axelrod1997
cargo build --release
uv sync
uv run axelrod-tools --help
```

## Caveats

- A file still in template form (`{{NAME}}` not yet substituted) cannot run on its own. In particular, Python import statements contain the placeholder, so even though the syntax is valid before substitution, it will raise a runtime error.
- `simulation/src/main.rs` contains only the minimal skeleton branching between the clap `run` / `sweep` subcommands. The simulation logic is implemented per paper. `run` must write `<output_dir>/config.json` and `sweep` must write `<output_dir>/sweep_config.json` (read by `show-experiment-settings`). On the `sweep` side, provide a path that emits `snapshots/step_*.csv` for each run via `--snapshot-interval N` (N>0) (required by the per-combination grid animation of `visualize-sweep`).
- `tools/src/<name>_tools/cli.py` is the dispatch skeleton for the `visualize` / `visualize-sweep` / `show-experiment-settings` subcommands. Add paper-specific subcommands such as `reproduce` as needed.
- `visualize_sweep.py` is a TODO file holding only the CLI skeleton and design-guidance comments. Fill in the parameter-dependency plot and the per-combination grid animation (`sweep_grid_animation.gif`) per paper (reference implementation: `replications/schelling1971/`).
- `show_experiment_settings.py` has only the general-purpose `--results-dir` mode. If you need to list paper-reproduction experiment definitions, create `reproduce_paper.py` and extend it by importing `Experiment` / `paper_experiments()` from there (see `replications/schelling1971/`).
- `_claude/` is a placeholder name to dodge the parent repository's `.gitignore` (which excludes all of `.claude/`). Always rename it to `.claude/` after copying.
- See `replications/schelling1971/` for a reference implementation.
