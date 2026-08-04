# creditforge

## About

Credit card reward rules are complex, change often, and are designed to
benefit the issuer more than the cardholder. Most people end up carrying
several cards without a real strategy — unsure which card to use for a
given purchase, whether a card is still worth keeping, or when the rules
have quietly changed underneath them.

**creditforge** is a personal credit-card strategy agent: it looks at the
cards you already have, your goals, and your spending habits, and tells
you what to do — which card to use, what to keep or drop, and whether a
change is actually worth the extra hassle it adds. It's built to optimize
spending you were already going to make, not to encourage spending more,
and "no action needed" is treated as a normal, valid answer rather than a
missed upsell.

This is an early-stage, actively developed project — see
[`CLAUDE.md`](CLAUDE.md) for the current state of the codebase.

## Local development

Environment variables are loaded via `.envrc` (direnv), which loads `.env`
if present (`cp .env.example .env`, then `direnv allow`). Full strategy —
what goes in `.env` vs `.envrc`, secret handling, Cloud Run plans — is in
[`docs/environment-variables/environment-variables.md`](docs/environment-variables/environment-variables.md).
Current variables:

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | `creditforge` | Application name (used in OpenAPI title) |
| `ENVIRONMENT` | `development` | Deployment environment name |
| `DATABASE_URL` | `postgresql+asyncpg://creditforge:creditforge@localhost:5432/creditforge` | Async Postgres connection string |

## License

Copyright © 2026 Dinabandhu Behera.

This project is licensed under the Apache License, Version 2.0.
See the [LICENSE](LICENSE) file for details.

Original project:
https://github.com/bandhu-workshop/creditforge

When using or discussing this project, attribution to the original repository
is appreciated.
