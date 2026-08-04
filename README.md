# creditforge

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
