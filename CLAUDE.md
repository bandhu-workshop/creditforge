# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

- Python 3.12, managed with `uv`
- FastAPI, PostgreSQL, Alembic, SQLModel, Pydantic, pydantic-settings
- Google ADK 2.x (stable)
- Tooling: ruff (lint/format), mypy (types), pytest (tests)

## Project Structure

### `src/creditforge/`

Layered backend package. Each layer has one job — don't reach across
layers (e.g. a route pulling DB internals directly instead of going
through `api/deps.py`):

- `main.py` — app-factory (`create_app()`) plus the module-level `app`
  ASGI entry point (`uvicorn creditforge.main:app`). Wires settings,
  logging, exception handlers, routers, and the DB-engine shutdown
  lifespan together; contains no logic of its own.
- `core/` — cross-cutting concerns: `config.py` (`Settings`, env-driven,
  see Environment variables below), `logging.py`, `exceptions.py`
  (`AppError` hierarchy + FastAPI handlers).
- `api/` — HTTP layer. `deps.py` holds shared FastAPI dependencies
  (e.g. `DbSession`); `health.py` is the unversioned health check;
  `v1/` is the versioned API — new endpoints get their own router under
  `v1/` and are registered on `v1/router.py`'s aggregator.
- `db/` — `base.py` holds the SQLModel metadata (import new models here
  so Alembic's autogenerate sees them); `session.py` is the async
  engine/session factory. DB access is async-only (`asyncpg` +
  `AsyncSession`) — no sync SQLAlchemy path, anywhere.
- `models/` — SQLModel ORM/table classes (one file per domain concept).
- `schemas/` — Pydantic request/response models. Kept separate from
  `models/` so API contracts don't leak DB column structure.
- `services/` — business logic and third-party integrations, orchestrates
  `models`/`db` and (eventually) the rules engine.
- `ai/` — Google ADK agentic code: `agents/` (agent definitions),
  `tools/` (functions agents call), `prompts/` (markdown templates).

All of the above except `main.py`/`core/` is currently an empty,
importable skeleton — no domain logic (`Card`/`Recommendation`/`Strategy`/
rules engine/auth) exists yet. Don't assume it does.

### `docs/` (repo root, committed to Git)

Canonical documentation for anyone who clones the repo to run or contribute
to the app: setup guides, environment-variable reference, API docs, etc.

Rule of thumb: if a new contributor needs it to use or build the app, it
belongs here — not in `localdev/`.

### `localdev/` (gitignored, not shipped)

Scratch space used while developing the application. Nothing here is
visible to anyone else who clones the repo, so it is for internal working
material only — never for anything a contributor needs to actually use or
build the app (that belongs in `docs/`).

Subfolders and their purpose:

- `debug/` — One subfolder per issue under investigation, named after the
  bug. Contains analysis notes, scripts, and temporary files used while
  debugging.
- `docs/` — One subfolder per piece of analysis, brainstorming, or
  planning. Kept up to date as the project evolves; serves as a running
  history of decisions and thinking.
- `experiments/` — One subfolder per proof-of-concept, named after the
  experiment. Used to try out ideas before they are adopted into the
  project.
- `features/` — One subfolder per feature being built. Holds all
  Superpowers-skill artifacts for that feature (brainstorming notes,
  architecture/design docs, TDD design, spec, implementation notes) plus
  the API contract, so a UI developer can start building against it.
- `temp/` — Throwaway code and files created on the fly: quick
  experiments, one-off scripts, anything not meant to persist.
- `logs/` — Local server logs streamed here for easier debugging.

## Environment

- Python `>=3.12`, pinned via `.python-version`.
- Dependencies and the virtual environment are managed with `uv`
  (`uv.lock` is committed).

### Environment variables

The canonical guide is `docs/environment-variables/environment-variables.md`.
When adding or changing configuration:

- Put local values and secrets in `.env`. Never commit `.env`.
- Update `.env.example` whenever a variable is added, renamed, or removed.
- Use `.envrc` only for direnv shell setup and non-secret developer
  tooling. It is committed to Git, so never place credentials, tokens,
  passwords, or API keys in it.
- Application code must read configuration from the process environment
  (see `Settings` in `src/creditforge/core/config.py`) and must not depend
  on `.env` or `.envrc` existing.
- Require variables via `Settings` fields with no default; never log
  secret values.
- Never copy `.env` into Docker images.
- For future Cloud Run deployment: use plain environment variables for
  non-sensitive configuration and Google Secret Manager for sensitive
  values.
- Preserve the commented-out GCP/Cloud Run reference section in `.envrc`.
  Do not uncomment it or implement Cloud Run deployment configuration
  unless the current task explicitly concerns deployment.

## Common Commands

```bash
uv sync              # Create or update .venv from pyproject.toml and uv.lock
uv add <package>     # Add a dependency
just dev             # Run the FastAPI app with reload (uvicorn)
just lint            # ruff check
just typecheck       # mypy src
just test            # pytest
just ci              # lint + typecheck + test (same gate CI runs)
just db-up           # Start local Postgres (docker compose)
just db-down         # Stop local Postgres
just migrate         # Apply Alembic migrations (alembic upgrade head)
just makemigrations "message"      # Generate a new migration
```

All frequently used commands are kept in the `Justfile` for convenience —
use it rather than retyping raw commands. Run `just ci` before considering
any change done; it's the same gate the `CI` GitHub Actions workflow runs.

## Testing

- `tests/unit/` mirrors `src/creditforge/`'s layout 1:1 (`tests/unit/api/`
  tests `src/creditforge/api/`, and so on) — put a new test next to its
  sibling, not in whichever file is open.
- `tests/integration/` is for cross-module tests that hit a real endpoint
  or a real DB; expected to stay empty until DB-dependent behavior exists.
- Tests are async-friendly by default: `asyncio_mode = "auto"` is set in
  `pyproject.toml`, so `async def test_...` needs no `@pytest.mark.asyncio`
  decorator.
- `tests/conftest.py`'s autouse fixture clears the `Settings`/DB-engine
  `lru_cache`s before and after every test — if a new cached singleton is
  added anywhere, clear it there too, or tests will silently leak state
  across each other.
- Prefer real behavior over mocks: build a real `FastAPI` app + `TestClient`
  for API tests, a real `AsyncEngine`/`AsyncSession` for DB tests (no live
  connection required — connections are lazy).

## Workflow Rules

### Browser-based debugging (Playwright MCP)

This repo has a `playwright` MCP server configured at project scope
(`.mcp.json`, committed — anyone opening the repo in Claude Code will be
prompted to approve it once). It drives a real, automatable browser
(navigate, click, screenshot, read console/network logs) — this is what to
use for deep, end-to-end debugging of the running application, not just
reading code.

**When to use it:** only when asked to debug, verify, or reproduce
something in a running instance of the app — e.g. "check why the login
page is blank," "confirm the ADK agent's streaming response renders
correctly." Do not reach for it for routine code changes; use it once
something needs to be *observed running*, not just read or edited.

**How to use it:** navigate to the relevant URL below, reproduce the issue,
and cross-reference with the corresponding logs/observability source and
the relevant code location so the fix targets the right layer (UI vs API
vs agent vs DB).

Debugging resources:

| Resource | Location |
|---|---|
| Backend code | `src/creditforge/` |
| Backend local URL | `http://localhost:8000` (via `just dev`; `/health`, `/api/v1/...`) |
| UI code | *(placeholder — no frontend exists in this repo yet)* |
| Frontend local URL | *(placeholder — no frontend exists yet)* |
| Application logs | `localdev/logs/` (intended location; nothing streams here yet — wire up file logging before relying on this) |
| ADK session details | *(placeholder — no ADK agent/session endpoint implemented yet; see `src/creditforge/ai/`)* |
| Phoenix observability | *(placeholder — not yet set up)* |

Update this table as each placeholder becomes real — don't leave it stale
once the frontend, ADK sessions, or Phoenix are actually wired up.

### Git and GitHub

- Never use the GitKraken MCP server; always use the `git`/`gh` CLI.
- The repo is public, with a solo-developer workflow: pull requests are
  required into `main`, 0 approvals are required, CI is the merge gate,
  squash-merge only, auto-merge after CI passes.
- Branch names: `feat/…`, `fix/…`, `refactor/…`, `docs/…`, `chore/…`.
- The PR title becomes the squash commit message on `main` — write it as
  a proper commit message (e.g. `feat: add password reset flow`).
- Full rationale, GitHub settings, and setup checklist:
  `docs/github-workflow/repo-branch-protection.md`.
- Never add a `Co-Authored-By: Claude …` (or any AI) trailer to commit
  messages, and never mention Claude/AI authorship in commits or PR
  descriptions. Claude/AI must never appear as a GitHub contributor on
  this repo — commit authorship stays solely with the human developer.

### Licensing

Project is Apache 2.0. SPDX header convention, NOTICE/CITATION.cff setup,
and rationale: `docs/licensing/apache-2.0-setup.md`.

### Docs organization

Inside `docs/`, each topic gets its own umbrella folder
(`docs/<topic>/<file>.md`) rather than a loose top-level `.md` file — even
for a single file today — so related material (diagrams, examples, more
docs on the same topic) has an obvious home later without a rename/move.
See `docs/environment-variables/`, `docs/github-workflow/`,
`docs/licensing/` for the pattern.
