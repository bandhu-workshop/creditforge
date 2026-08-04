# GitHub repo & branch protection setup (solo-developer workflow)

Status log and rationale for how this repo is configured on GitHub. Update this
file whenever the setup changes; keep `CLAUDE.md` pointing here instead of
duplicating the details.

## Decisions made so far

- **2026-08-03**: Repo `bandhu-workshop/creditforge` switched from private to
  public. Reason: needed for GitHub auto-merge on the Free plan, and to allow
  branch protection rulesets without a paid plan. Verified no secrets,
  `.env` files, keys, or credentials exist in tracked files or git history
  before flipping visibility.
- Branch ruleset for `main` and a required `CI` status check are **not yet
  set up** — no `.github/workflows` exists yet in this repo. This is the next
  step once a CI workflow is scaffolded.

## Target end state (solo-dev, AI-assisted)

The goal: require PRs into `main`, but require **zero human approvals**. Let CI
protect `main`, use AI for review, use GitHub auto-merge after checks pass.
Rationale: gives clean history, PR descriptions, test evidence, and rollback
context without pretending another human reviewer exists.

### 1. Repo merge settings (Settings → General → Pull Requests)

| Setting | Value |
|---|---|
| Allow squash merging | On |
| Default squash message | Pull request title and description |
| Allow merge commits | Off |
| Allow rebase merging | Off |
| Allow auto-merge | On |
| Automatically delete head branches | On |

Squash merging turns a PR's WIP commits into one clean commit on `main`.
Since squash merge is used, **the PR title becomes the permanent commit
message** — write it accordingly (see commit/PR title format below).

### 2. Branch ruleset for `main` (Settings → Rules → Rulesets → New branch ruleset)

Target: default branch (`main`). Enable:

- Restrict deletions
- Block force pushes
- Require a pull request before merging
- Required approvals: **0**
- Require status checks to pass — required check: **`CI`**

Do **not** enable (not needed for a solo project): code-owner approval,
signed commits, merge queue, required deployments, multiple approving
reviews, required branch updates, admin/AI bypass.

Optional: enable "Require conversation resolution before merging" if AI/PR
review comments are used regularly — forces intentional resolution instead of
ignoring them.

**Blocker as of 2026-08-03**: this ruleset needs a required status check named
`CI`. No CI workflow exists yet — set one up first (see below), then add the
ruleset.

### 3. One CI workflow, one required check

Avoid separate required checks per step (lint, types, tests, build). Use a
single workflow named `CI` that runs, in order:

```
install deps → lint/format check → type check → unit tests → build/package check
```

Minimum practical jobs for this project: lint (ruff), type check (mypy),
unit tests (pytest). Add integration tests / security scans / coverage gates
only when actually needed.

### 4. PR template

`.github/pull_request_template.md` — keep it short (what changed / why /
validation checklist / risk & rollback). Avoid a long checklist; it gets
rubber-stamped past 5-6 items.

### 5. AI-assisted workflow loop

```
feature branch → implement with coding agent → open PR (generated description)
→ CI runs → AI review of diff → resolve comments on high-risk areas
→ enable auto-merge → GitHub squash-merges once CI passes
```

Trust boundary: AI writes code/tests/PR description, reviews changes, suggests
fixes. GitHub enforces CI, blocks direct pushes to `main`, performs
auto-merge. One human action stays in the loop: enabling auto-merge after a
quick glance at the PR — this stops an agent from autonomously creating,
reviewing, and merging its own possibly-wrong change unsupervised.

### 6. Deliberately skipped (revisit only if actually needed)

CODEOWNERS, multiple PR templates, mandatory issue-per-change, mandatory
labels, release/`develop` branches, merge queues, mandatory commit signing,
AI branch-protection bypass, required manual approval, semantic-version
automation.

### Branch & commit naming

Short-lived branches off `main`: `feat/…`, `fix/…`, `refactor/…`, `docs/…`.
PR titles (become the squash commit message): `feat: add password reset
flow`, `fix: handle expired access tokens`, etc.

## Open follow-ups

- [x] Scaffold `.github/workflows/ci.yml` (job name `ci`, runs ruff/mypy/pytest
      via `uv`). Added dev dependency group (ruff, mypy, pytest) and tool
      config to `pyproject.toml`; `src/creditforge/__init__.py` +
      `tests/test_smoke.py` added as placeholders so lint/type/test all have
      something to check. Verified locally and in Actions (run
      `30840063744`, success).
- [x] Add branch ruleset on `main` (2026-08-03, ruleset id `20318764`):
      block deletion + non-fast-forward, require PR with 0 approvals, require
      status check `ci`. Verified: a direct push to `main` from a fresh clone
      is rejected with `GH013` ("Changes must be made through a pull
      request" + "Required status check \"ci\" is expected").
- [x] Add `.github/pull_request_template.md` (What changed / Why /
      Validation / Risk and rollback).
- [x] Set repo merge settings (2026-08-03): squash merge only (merge commit
      and rebase merge disabled), auto-merge enabled, auto-delete head
      branches enabled, squash commit title/message = PR title/body.

All items from the target end state are now live. Remaining manual step per
PR: enable auto-merge after a quick review (see AI-assisted workflow loop
above) — this is intentionally not automated.
