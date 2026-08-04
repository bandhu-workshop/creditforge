# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack
  - python 3.12, uv
  - fastapi, postgress, alembic, sqlmodel, pydantic, pydantic-settings, etc
  - google adk 2.x (stable)
  - ruff, mypy, pytest 

## Project Structure
- src
  - all backend related codes
- docs (repo root, committed to Git)
  - Canonical docs for anyone who clones the repo to run or contribute to
    the app: setup guides, env-var reference, API docs, etc. Rule of thumb:
    if a new contributor would need it to use/build the app, it goes here,
    not in `localdev/`.
- localdev
  The `localdev/` tree (`debug/`, `docs/`, `docs/planning/`, `experiments/`, `features/`, `scripts/`, `temp/`, `logs/`) holds ad hoc,
  non-shipped work. This is the scratch-pad directory, which we use while developing the application, this keeps important files, only the `tmp/` folder contains throwaway codes and files.
  `localdev/` is gitignored — nothing here is visible to anyone else who
  clones the repo, so it's for internal working docs (brainstorms, design
  decisions, planning history), never for anything a contributor needs to
  actually use or build the app (that goes in the root `docs/` above).

  - All folders have their role
    - debug: We use this folder for debugging issues we are facing in the application, generally we will create a folder with name representing the bug we are facing and inside that folder we will have analysis files and script files and temp files which were used for etc.
    - docs: In this folder we will create sub-folders with proper name of analysis or brainstorming we are doing or planning we are doing, all sort of documentation which we might need later, with our project changing we will keep this docs updated and keep thinking and planning hiostory. 
    - experiemnts: the experiemnt folder where we do small proof-of-concepts, the POCs will be sub-folders with appropriate naming and inside that folder we will have our experiemnts and pocs before including in project.
    - features: Inside this we will create sub-folders with proper name of feature we are building and all the superpower skill's things will stay inside these subfolders, for example, brainstorming, architecture and design planning, TDD design, spec building, implementation etc. This folder also will contain the API contract so that UI developer can start developing using this.
    - temp: This folder will keep the throw away code which are creted during brainstorming or on the fly to test things or to fetch or to observe things or in any case
    - logs: This is the folder we use to stream logs from local servers for better debugging and all

## Environment

- Python `>=3.12` (pinned to 3.12 via `.python-version`).
- Dependency/environment management is via `uv` (`uv.lock` present).

## Environment-variable rules

The canonical environment-variable guide is `docs/environment-variables.md`.

When creating or modifying configuration:
  - Use `.env` for local values and secrets. Never commit `.env`.
  - Update `.env.example` whenever a variable is added, renamed, or removed.
  - Use `.envrc` only for direnv shell setup and non-secret developer
    tooling. Never place credentials, tokens, passwords, or API keys in
    `.envrc` — it is committed to Git.
  - Application code must read configuration from the process environment
    (`Settings` in `src/creditforge/core/config.py`) — never make it depend
    on `.env`/`.envrc` existing.
  - Validate required variables via `Settings` fields with no default; never
    log secret values.
  - Do not copy `.env` into Docker images.
  - For future Cloud Run deployment: normal environment variables for
    non-sensitive config, Google Secret Manager for sensitive values.
  - Preserve the commented GCP/Cloud Run reference section in `.envrc`; do
    not uncomment or implement Cloud Run deployment configuration unless
    the current task explicitly concerns deployment.

## Common commands:

```bash
uv sync              # create/update .venv from pyproject.toml + uv.lock
just dev              # run the FastAPI app with reload (uvicorn)
uv add <package>     # add a dependency
```
- we will keep all the common commands in `Justfile` for conveniencea and use repeadely when ever needed.

## Workflow Rules

1. Git and gh rules
  - Never use the git-kraken MCP server; always use `git`/`gh` CLI.
  - Repo is public. Solo-dev flow: PRs required into `main`, 0 required
    approvals, CI is the gate, squash-merge only, auto-merge after CI passes.
  - Branch names: `feat/…`, `fix/…`, `refactor/…`, `docs/…`, `chore/…`.
  - PR title = squash commit message on `main` — write it as a proper
    commit message (e.g. `feat: add password reset flow`).
  - Full rationale, GitHub settings, and setup checklist:
    `localdev/docs/github-workflow/repo-branch-protection.md`.
  - Never add a `Co-Authored-By: Claude ...` (or any AI) trailer to commit
    messages, and never mention Claude/AI authorship in commits or PR
    descriptions. Claude/AI must never show up as a GitHub contributor on
    this repo — commit authorship stays solely the human developer's.




