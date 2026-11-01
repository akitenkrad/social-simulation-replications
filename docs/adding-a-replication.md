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
| `{{NAME}}` | The slug: package prefix without the `rep-` key prefix (lowercase letters recommended) | `axelrod`, `schelling` |

A single `{{NAME}}` derives the following identifiers:

- Rust crate: `<NAME>-simulation`
- Rust binary: `<NAME>`
- Python package: `<NAME_snake>_tools` (directory name / module name; hyphens in `<NAME>` become underscores)
- Python CLI: `<NAME>-tools`

## Naming

Every replication has two identifiers. They are different values and must not be confused.

| Identifier | Rule | Example | Used for |
|------------|------|---------|----------|
| key (`<key>`) | `rep-{first author's surname, lowercase}{year}` | `rep-axelrod1997` | directory name, submodule path, GitHub repository name, runvault `repo_id`, and `key` / `repo` in `replications.toml` |
| slug (`<name>`) | short lowercase name, **no** `rep-` prefix | `axelrod` | Rust crate, binary, and Python package names (the `{{NAME}}` placeholder) |

- The surname is written in lowercase ASCII letters with spaces and hyphens removed (Noelle-Neumann → `rep-noelleneumann1974`).
- Exception: a system reconstructed from several papers uses the system name instead (`rep-logistello`).
- The key matches `^rep-[a-z0-9]+(-[a-z0-9]+)*$`; `repo` in `replications.toml` is the same string as `key`.
- Because the key is the runvault `repo_id`, and runvault-socsim namespaces experiment-local event kinds as `x.<repo_id>.<kind>`, renaming a repository changes its event kinds. Readers of run output should not hard-code them.

## Usage (manual setup)

Steps to create a new project under `replications/<key>/`. `<key>` is the key (e.g. `rep-axelrod1997`), and `<name>` is the slug (e.g. `axelrod`); see [Naming](#naming).

```bash
# Intended to be run from the parent repository root

# 1. Copy the template
cp -R template/files replications/<key>

# 2. Replace the {{NAME}} placeholder with <name> everywhere
#    (macOS sed needs the -i '' form; on Linux -i alone is fine)
find replications/<key> -type f -exec sed -i '' \
  -e 's/{{NAME}}_tools/<name_snake>_tools/g' -e 's/{{NAME}}/<name>/g' {} \;

# 3. Rename the Python package directory
mv replications/<key>/tools/src/_NAME_tools \
   replications/<key>/tools/src/<name_snake>_tools

# 4. Rename _claude/ to .claude/ (the placeholder name dodges the parent repo's .gitignore)
mv replications/<key>/_claude replications/<key>/.claude

# 5. Verify the build and dependency resolution
cd replications/<key>
cargo build --release
uv sync
uv run <name>-tools --help
```

### 6. Initialize and commit the replication repository

The scaffolded directory becomes the root of the new repository. Create its first commit before registering it as a submodule:

```bash
# Still inside replications/<key>
git init
git add .
git commit -m "Initial replication implementation"
```

### 7. Create and push the GitHub repository

Create `akitenkrad/<key>` with the appropriate visibility and push the first commit. Choose either `--public` or `--private` for the repository being created:

```bash
gh repo create akitenkrad/<key> --public --source . --push
# Or replace --public with --private.
```

You can instead create the repository separately, add it as `origin`, and push the current branch.

### 8. Register the repository as a submodule

Return to the parent monorepo and add the submodule at the scaffolded path:

```bash
cd ../..
git submodule add git@github.com:akitenkrad/<key>.git replications/<key>
```

`git submodule add` accepts an existing Git repository at the destination path, so the directory created and committed in the preceding steps does not need to be removed or cloned again.

### 9. Register the replication in the catalog

The replication tables in `README.md`, `README.ja.md`, and `docs/replications*.md` are auto-generated from `replications.toml` at the repo root. Do **not** edit those tables by hand. Instead:

```bash
# Append a [[replication]] entry to replications.toml (see existing entries for the
# field list: key, repo, author, year, year_display?, title, paradigm, domain, theme_en, theme_ja)
# then regenerate every catalog target:
python3 tools/gen_catalog.py

# Verify nothing is stale (useful in CI):
python3 tools/gen_catalog.py --check
```

### 10. Commit the parent monorepo changes

The parent commit records the submodule configuration and pointer together with the catalog source and generated files:

```bash
git add .gitmodules replications/<key> replications.toml \
  README.md README.ja.md docs/replications.md docs/replications.ja.md
git commit -m "Add <key> replication"
```

### Example: Axelrod (1997)

Key `rep-axelrod1997`, slug `axelrod`:

```bash
cp -R template/files replications/rep-axelrod1997
find replications/rep-axelrod1997 -type f -exec sed -i '' 's/{{NAME}}/axelrod/g' {} \;
mv replications/rep-axelrod1997/tools/src/_NAME_tools \
   replications/rep-axelrod1997/tools/src/axelrod_tools
mv replications/rep-axelrod1997/_claude replications/rep-axelrod1997/.claude

cd replications/rep-axelrod1997
cargo build --release
uv sync
uv run axelrod-tools --help

git init
git add .
git commit -m "Initial replication implementation"
gh repo create akitenkrad/rep-axelrod1997 --public --source . --push

cd ../..
git submodule add git@github.com:akitenkrad/rep-axelrod1997.git replications/rep-axelrod1997
```

The corresponding `replications.toml` entry uses the key for both `key` and `repo`:

```toml
[[replication]]
key = "rep-axelrod1997"
repo = "rep-axelrod1997"
author = "Axelrod"
year = 1997
title = "The Dissemination of Culture"
paradigm = "classic-abm"
domain = ""
theme_en = "Cultural dissemination"
theme_ja = "文化の伝播"
```

## Caveats

- A file still in template form (`{{NAME}}` not yet substituted) cannot run on its own. In particular, Python import statements contain the placeholder, so even though the syntax is valid before substitution, it will raise a runtime error.
- `simulation/src/main.rs` contains only the minimal skeleton branching between the clap `run` / `sweep` subcommands. The simulation logic is implemented per paper. `run` must write `<output_dir>/config.json` and `sweep` must write `<output_dir>/sweep_config.json` (read by `show-experiment-settings`). On the `sweep` side, provide a path that emits `snapshots/step_*.csv` for each run via `--snapshot-interval N` (N>0) (required by the per-combination grid animation of `visualize-sweep`).
- `tools/src/<name>_tools/cli.py` is the dispatch skeleton for the `visualize` / `visualize-sweep` / `show-experiment-settings` subcommands. Add paper-specific subcommands such as `reproduce` as needed.
- `visualize_sweep.py` is a TODO file holding only the CLI skeleton and design-guidance comments. Fill in the parameter-dependency plot and the per-combination grid animation (`sweep_grid_animation.gif`) per paper (reference implementation: `replications/rep-schelling1971/`).
- `show_experiment_settings.py` has only the general-purpose `--results-dir` mode. If you need to list paper-reproduction experiment definitions, create `reproduce_paper.py` and extend it by importing `Experiment` / `paper_experiments()` from there (see `replications/rep-schelling1971/`).
- `_claude/` is a placeholder name to dodge the parent repository's `.gitignore` (which excludes all of `.claude/`). Always rename it to `.claude/` after copying.
- See `replications/rep-schelling1971/` for a reference implementation.
