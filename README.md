# creditforge

## Local development

Environment variables are loaded via `.envrc` (direnv) — no `.env` file is
used. Required variables:

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://creditforge:creditforge@localhost:5432/creditforge` | Async Postgres connection string |
| `ENVIRONMENT` | `development` | Deployment environment name |

## License

Copyright © 2026 Dinabandhu Behera.

This project is licensed under the Apache License, Version 2.0.
See the [LICENSE](LICENSE) file for details.

Original project:
https://github.com/bandhu-workshop/creditforge

When using or discussing this project, attribution to the original repository
is appreciated.
