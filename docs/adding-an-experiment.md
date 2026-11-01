**English** | [日本語](adding-an-experiment.ja.md)

# Adding an Experiment

The shared template also scaffolds original social-simulation experiments that have no source paper. It provides the same two-project layout as replications: a Cargo workspace and a uv workspace containing a Rust simulation plus Python tooling.

## Layout

```
template/
├── README.md                      ← guide to the shared template
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
```

## Naming

Every experiment has two identifiers. They are different values and must not be confused.

| Identifier | Rule | Example | Used for |
|------------|------|---------|----------|
| key (`<key>`) | `exp-{subject}-{change}`, lowercase kebab-case, 2–4 words after the prefix | `exp-dollar-auction-escalation` | directory name, submodule path, GitHub repository name, runvault `repo_id`, and `key` / `repo` in `replications.toml` |
| slug (`<name>`) | short lowercase name, **no** `exp-` prefix | `dollar-auction` | Rust crate, binary, and Python package names (the `{{NAME}}` placeholder) |

- *subject* is the game or model being run (`dollar-auction`, `rumor`); *change* is what departs from the textbook setting (`escalation`, `forgetting`).
- The key matches `^exp-[a-z0-9]+(-[a-z0-9]+)*$`; `repo` in `replications.toml` is the same string as `key`.
- The five experiments that predate this rule were renamed to `exp-<old key>` and otherwise kept as they are, so not all of them read as subject–change.
- Because the key is the runvault `repo_id`, and runvault-socsim namespaces experiment-local event kinds as `x.<repo_id>.<kind>`, renaming a repository changes its event kinds. Readers of run output should not hard-code them.

The slug allows hyphens but not underscores (for example `dollar-auction`). `<name_snake>` is the same value with hyphens replaced by underscores (`dollar_auction`); it is used only for the Python module directory and the `[project.scripts]` target. `tools/review-kit` checks that all derived names come from the one slug.

## Usage (manual setup)

```bash
# Intended to be run from the parent repository root

# 1. Copy the template
mkdir -p experiments
cp -R template/files experiments/<key>

# 2. Replace the {{NAME}} placeholder with <name> everywhere
#    (macOS sed needs the -i '' form; on Linux -i alone is fine)
find experiments/<key> -type f -exec sed -i '' \
  -e 's/{{NAME}}_tools/<name_snake>_tools/g' -e 's/{{NAME}}/<name>/g' {} \;

# 3. Rename the Python package directory
mv experiments/<key>/tools/src/_NAME_tools \
   experiments/<key>/tools/src/<name_snake>_tools

# 4. Rename _claude/ to .claude/ (the placeholder name dodges the parent repo's .gitignore)
mv experiments/<key>/_claude experiments/<key>/.claude

# 5. Verify the build and dependency resolution
cd experiments/<key>
cargo build --release
uv sync
uv run <name>-tools --help
```

### 6. Initialize and commit the experiment repository

```bash
# Still inside experiments/<key>
git init
git add .
git commit -m "Initial experiment implementation"
```

### 7. Create and push the GitHub repository

Create `akitenkrad/<key>` with the appropriate visibility and push the first commit. Choose either `--public` or `--private` for the repository being created:

```bash
gh repo create akitenkrad/<key> --public --source . --push
# Or replace --public with --private.
```

You can instead create the repository separately, add it as `origin`, and push the current branch.

### 8. Register the repository as a submodule

```bash
cd ../..
git submodule add git@github.com:akitenkrad/<key>.git experiments/<key>
```

`git submodule add` accepts an existing Git repository at the destination path, so the scaffolded and committed directory does not need to be removed or cloned again.

### 9. Register the experiment in the catalog

Add all six required fields to `replications.toml`:

```toml
[[experiment]]
key = "exp-dollar-auction-escalation"
repo = "exp-dollar-auction-escalation"
year = 2026
title = "LLM-Agent Escalation in the Dollar Auction"
theme_en = "Escalation and sunk-cost behavior"
theme_ja = "エスカレーションと埋没費用行動"
```

Then regenerate and check every catalog target:

```bash
python3 tools/gen_catalog.py
python3 tools/gen_catalog.py --check
```

### 10. Commit the parent monorepo changes

```bash
git add .gitmodules experiments/<key> replications.toml \
  README.md README.ja.md docs/experiments.md docs/experiments.ja.md
git commit -m "Add <key> experiment"
```

### Example: dollar-auction escalation

Key `exp-dollar-auction-escalation`, slug `dollar-auction` (`dollar_auction` in snake form):

```bash
cp -R template/files experiments/exp-dollar-auction-escalation
find experiments/exp-dollar-auction-escalation -type f -exec sed -i '' \
  -e 's/{{NAME}}_tools/dollar_auction_tools/g' -e 's/{{NAME}}/dollar-auction/g' {} \;
mv experiments/exp-dollar-auction-escalation/tools/src/_NAME_tools \
   experiments/exp-dollar-auction-escalation/tools/src/dollar_auction_tools
mv experiments/exp-dollar-auction-escalation/_claude experiments/exp-dollar-auction-escalation/.claude
```

The repository is then created as `akitenkrad/exp-dollar-auction-escalation` and added with
`git submodule add git@github.com:akitenkrad/exp-dollar-auction-escalation.git experiments/exp-dollar-auction-escalation`.

## Run recording

Runvault wiring is not part of the template. Follow `replications/rep-schelling1971/`, including its `runvault.toml`, the Rust `runvault` dependency, and the Python `runvault[read]` dependency when the experiment needs managed run output. Always pass `--scratch` for development, debugging, and smoke-test runs; scratch runs are stored under `results/_scratch/` and are not synced.

## Caveats

- A file still in template form (`{{NAME}}` not yet substituted) cannot run on its own.
- Implement project-specific simulation logic and analysis commands after scaffolding.
- `_claude/` is a placeholder name that avoids the parent repository's `.gitignore`; always rename it to `.claude/` after copying.
- See `replications/rep-schelling1971/` for a complete implementation of the shared scaffold and runvault integration.
