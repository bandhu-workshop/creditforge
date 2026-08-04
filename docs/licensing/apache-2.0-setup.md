# Licensing setup — Apache License 2.0

## Decision

- **2026-08-04**: creditforge is open-sourced under **Apache License 2.0**.
- Goal: whoever uses or builds on this repo/idea should credit the original
  project. Apache 2.0 was chosen over MIT because of its `NOTICE` file
  mechanism — anyone redistributing the source must carry the attribution
  notice forward. MIT only requires keeping the copyright/license text in
  copies of the source; it has no equivalent attribution-carrying mechanism.
- A fully custom "mandatory public credit" license was considered and
  rejected: no OSI license can force credit in a downstream product's
  README/marketing/UI unless that party actually redistributes the licensed
  source, and a clause that tried to force this further would stop being
  real open source. Apache 2.0 + NOTICE is the standard, still-genuinely-open
  way to get as close as license terms allow; a plain-language "attribution
  appreciated" note was added to the README as the (non-binding) ask for the
  rest.

## What was added, and why

| File | Purpose |
|---|---|
| `LICENSE` | Full, unmodified Apache License 2.0 text with the copyright line filled in (Appendix section). |
| `NOTICE` | Project name, copyright, canonical repo URL, and the attribution ask. Must be carried forward by anyone redistributing the source, per License §4(d). |
| `CITATION.cff` | Machine-readable citation metadata. GitHub auto-detects a root-level `CITATION.cff` and surfaces a "Cite this repository" button/BibTeX/APA export on the repo page. |
| `README.md` | Human-readable license section pointing at `LICENSE`, plus the same attribution ask in plain language. |
| SPDX headers (`# SPDX-FileCopyrightText:` / `# SPDX-License-Identifier: Apache-2.0`) | Added to the top of real source/config files so license info travels with the file even if copied out of the repo individually: `pyproject.toml`, `Justfile`, `.github/workflows/ci.yml`, `src/creditforge/__init__.py`, `tests/test_smoke.py`. |
| `pyproject.toml` `license = "Apache-2.0"` | PEP 639 SPDX license expression in project metadata, so packaging tools (pip, uv, PyPI) surface the license correctly. |

SPDX headers were **not** added to `CLAUDE.md` or files under `localdev/` —
those are internal working notes/instructions, not shipped project artifacts.

## What this setup does and doesn't guarantee

- Does: legally require anyone who redistributes the Source form (as-is or
  modified) to keep copyright/license/NOTICE text intact, and to mark
  changed files as changed.
- Does: give GitHub / citation tools a canonical, machine-readable way to
  credit the project (`CITATION.cff`, SPDX headers, license metadata).
- Does not: force someone who merely uses the *idea*, or a product built on
  top without redistributing the actual source, to publicly mention this
  repo. No standard open-source license can do that — the README's
  "attribution is appreciated" line is a social ask, not an enforceable term.

## Third-party notices

No third-party code, models, or assets are vendored into this repo yet. If
that changes (e.g. copied snippets, bundled model weights, non-Apache
dependencies with redistribution requirements), add a `THIRD_PARTY_NOTICES.md`
at the repo root listing them — do not fold their license text into `NOTICE`,
which is reserved for this project's own attribution notice.

## Follow-ups

- [ ] Add SPDX headers to new source files as they're created (see list of
      file types above for the comment syntax per language).
- [ ] If a third-party dependency or asset with its own attribution
      requirement is added, create `THIRD_PARTY_NOTICES.md`.
