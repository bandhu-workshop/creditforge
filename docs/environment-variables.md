# Environment Variable Management

## Purpose

This document defines how application configuration and secrets are managed during:

* Local development
* Automated testing
* CI/CD
* Future Google Cloud Run deployment

The primary objective is to keep configuration simple while ensuring that secrets never enter source control, Docker images, logs, or pull-request descriptions.

---

## File responsibilities

### `.env`

The `.env` file contains developer-specific local application configuration.

Examples include:

* Local database URLs
* API keys (once the application has any)
* Development feature flags
* Local service endpoints
* Debug settings

The `.env` file must never be committed.

Example:

```dotenv
APP_NAME=creditforge
ENVIRONMENT=development
DATABASE_URL=postgresql+asyncpg://creditforge:creditforge@localhost:5432/creditforge
```

### `.env.example`

The `.env.example` file documents every supported environment variable.

It must:

* Be committed to Git
* Contain variable names
* Contain safe defaults where appropriate
* Leave secret values empty
* Be updated whenever a variable is added, renamed, or removed

A new developer should be able to create their local configuration with:

```bash
cp .env.example .env
```

### `.envrc`

The `.envrc` file configures the local development shell through direnv.

It is responsible for:

* Loading `.env` (via `dotenv_if_exists .env`)
* Activating the local Python virtual environment
* Setting development-only shell paths
* Retaining commented GCP and Cloud Run references for future deployment work

It must not contain:

* Passwords
* API keys
* Access tokens
* Private keys
* Database credentials
* Service-account JSON content

The `.envrc` file is committed to Git.

### `docs/environment-variables.md` (this file)

This document is the canonical source for the environment-variable strategy.

Detailed operational guidance belongs here rather than in `CLAUDE.md`.

### `CLAUDE.md`

`CLAUDE.md` contains concise rules for coding agents.

It points agents to this document and prevents them from introducing unsafe configuration patterns.

---

## Local-development workflow

### Initial setup

Install direnv and connect it to the shell.

For Bash, add this to `~/.bashrc`:

```bash
eval "$(direnv hook bash)"
```

For Zsh, add this to `~/.zshrc`:

```bash
eval "$(direnv hook zsh)"
```

Restart the shell after adding the hook.

Direnv requires both installation and a shell hook before `.envrc` can be loaded automatically. ([direnv][3])

### Create the local environment

```bash
cp .env.example .env
```

Fill in the required local values:

```bash
nano .env
```

Create the Python environment (already handled by `uv sync`, but for reference):

```bash
uv sync
```

Enter the project and approve its `.envrc`:

```bash
direnv allow
```

Direnv will then load the project environment when entering the directory and unload it when leaving.

### Reload after configuration changes

After editing `.envrc`, approve the changed file:

```bash
direnv allow
```

After editing `.env`, reload the environment:

```bash
direnv reload
```

### Verify the environment

```bash
direnv status
```

Check an individual non-secret variable:

```bash
printenv ENVIRONMENT
```

Do not print secret variables into terminal recordings, CI logs, screenshots, or support messages.

---

## Application design rule

The application must read configuration from operating-system environment variables.

The application must not require `.env` or `.envrc` to exist.

This is important because:

* Local development receives variables through direnv.
* Tests may inject variables directly (see `tests/conftest.py`'s settings-cache-clearing fixture).
* CI/CD provides variables through its own configuration.
* Cloud Run injects variables into the container runtime.

This project's `Settings` (`src/creditforge/core/config.py`, built on `pydantic-settings`) intentionally has **no `env_file` configured** — it only reads real process environment variables. `.env` loading is direnv's job (`dotenv_if_exists .env` in `.envrc`), not pydantic-settings'. This avoids two independent, possibly-inconsistent `.env`-loading code paths.

For required values, the application should validate configuration during startup and fail with a clear error — `pydantic-settings` already does this for any `Settings` field without a default.

---

## Variable classification

Every environment variable belongs to one of the following classifications.

### Public application configuration

Examples in this project:

```text
APP_NAME
ENVIRONMENT
```

These values are not confidential. For Cloud Run, they can later be configured as ordinary service environment variables.

### Sensitive configuration

Examples (current and anticipated):

```text
DATABASE_URL
```

(Future, once wired up: LLM/Google ADK API keys, any external partner API tokens.)

These must:

* Remain in the ignored local `.env` during local development
* Be stored in the CI/CD secret store during automation
* Be stored in Google Secret Manager for Cloud Run
* Never be committed
* Never be placed directly in deployment commands kept in shell history

Google recommends Secret Manager rather than ordinary Cloud Run environment-variable configuration for passwords, API keys, and other sensitive values. ([Google Cloud Documentation][4])

### Runtime-provided variables

Examples for Cloud Run include:

```text
PORT
K_SERVICE
K_REVISION
K_CONFIGURATION
```

These are supplied by the Cloud Run runtime and must not be treated as locally managed secrets or configuration. ([Google Cloud Documentation][5]) Not relevant yet — this project has no Cloud Run deployment, and locally the port is chosen by `just dev` (uvicorn), not read from `Settings`.

---

## Naming convention

Environment-variable names must:

* Use uppercase letters
* Use underscores between words
* Describe one value
* Include units when the unit is not obvious

Preferred:

```text
DATABASE_URL
REQUEST_TIMEOUT_SECONDS
CACHE_TTL_SECONDS
GOOGLE_CLOUD_PROJECT
```

Avoid:

```text
db
timeout
config
value1
secret
```

Boolean values should use a consistent representation:

```dotenv
FEATURE_ENABLED=true
```

Application parsing should accept and normalize the expected representation.

---

## Adding a new variable

Whenever a new environment variable is introduced:

1. Add it to `.env.example`.
2. Add a description to this document when its purpose is not obvious.
3. Add it to the `Settings` model (`src/creditforge/core/config.py`).
4. Decide whether it is required or optional.
5. Provide a safe default only when one genuinely exists.
6. Add it to your local `.env`.
7. Add it to test or CI configuration when required.
8. Later, add it to Cloud Run configuration or Secret Manager.
9. Confirm that its value is not logged.
10. Include the configuration change in the pull-request description.

The pull request should explain:

```text
New variable: VARIABLE_NAME
Classification: public configuration | secret
Required: yes | no
Default: value or none
Deployment action: required or not required
```

---

## Removing or renaming a variable

A variable must not be deleted or renamed without checking:

* Application references (`Settings` fields)
* Tests
* Docker configuration (once a Dockerfile exists)
* CI workflows
* Deployment configuration
* Documentation (this file, `.env.example`, `README.md`)
* Cloud Run revisions
* Secret Manager secrets

For renames, use a temporary compatibility period when an existing deployed environment may still provide the old name.

---

## Secret-handling rules

Never:

* Commit `.env`
* Put real secrets in `.env.example`
* Put secrets in `.envrc`
* Put secrets in `CLAUDE.md`
* Put secrets in documentation
* Bake secrets into Docker images
* Pass secrets as Docker build arguments
* Print secrets in application logs
* Include secrets in exception messages
* Paste secrets into pull requests or issues
* Store service-account JSON files in the repository

When a secret is accidentally committed:

1. Treat the secret as compromised.
2. Revoke or rotate it immediately.
3. Remove it from the repository history where appropriate.
4. Review logs and recent usage.
5. Add a preventive ignore or scanning rule.

Deleting the visible line from the latest commit is not sufficient because the value may still exist in Git history.

---

## Docker rules (once a Dockerfile exists)

No Dockerfile exists in this project yet. When one is added, the image must not contain:

```text
.env
.envrc
.env.*
service-account JSON files
developer credentials
```

`.dockerignore` (already added, ready for when a Dockerfile lands) covers this. The application container must receive configuration at runtime — do not copy `.env` into the image and do not use it as a build-time secret source.

---

## Cloud Run strategy

Cloud Run deployment will be implemented later.

The intended separation is:

### Non-sensitive configuration

Configure ordinary settings as Cloud Run service environment variables.

Examples:

```text
APP_NAME=creditforge
ENVIRONMENT=production
GOOGLE_CLOUD_PROJECT=project-id
```

### Sensitive configuration

Store sensitive values in Google Secret Manager and grant the Cloud Run service identity access only to the required secrets.

The Cloud Run service account will require the minimum permissions needed by the application. Access to secrets is granted using the Secret Manager Secret Accessor role for the specific service identity. ([Google Cloud Documentation][6])

### Google Cloud authentication

Local development may use:

```bash
gcloud auth application-default login
```

Cloud Run must use its assigned service identity.

Do not configure `GOOGLE_APPLICATION_CREDENTIALS` in Cloud Run and do not deploy local service-account key files.

### Port handling

Cloud Run supplies the `PORT` variable.

If/when the application needs to read it directly rather than relying on the ASGI server's own port binding, use:

```python
port = int(os.getenv("PORT", "8000"))
```

The fallback (`8000`) supports local development, while the Cloud Run-provided value controls the deployed container.

---

## Recommended repository structure

```text
creditforge/
├── .env
├── .env.example
├── .envrc
├── .gitignore
├── .dockerignore
├── CLAUDE.md
├── docs/
│   └── environment-variables.md
└── src/
```

Repository status:

| File                            | Commit? | May contain secrets? |
| ------------------------------- | ------: | -------------------: |
| `.env`                          |      No |      Yes, local only |
| `.env.example`                  |     Yes |                   No |
| `.envrc`                        |     Yes |                   No |
| `.gitignore`                    |     Yes |                   No |
| `.dockerignore`                 |     Yes |                   No |
| `docs/environment-variables.md` |     Yes |                   No |
| `CLAUDE.md`                     |     Yes |                   No |

---

## Final policy

The project follows this configuration chain:

```text
Local .env
    ↓
direnv loads variables through .envrc
    ↓
application reads operating-system environment
```

Future production configuration will follow:

```text
Cloud Run environment variables + Secret Manager
    ↓
Cloud Run injects runtime configuration
    ↓
application reads operating-system environment
```

The application therefore uses one configuration interface — the process environment — regardless of whether it is running locally, in tests, in CI, or on Cloud Run.

## References

[1]: https://direnv.net/man/direnv-stdlib.1.html "DIRENV-STDLIB 1 “2019” direnv “User Manuals” | direnv"
[2]: https://docs.cloud.google.com/run/docs/developing "Developing your service | Cloud Run"
[3]: https://direnv.net/docs/installation.html "Installation"
[4]: https://docs.cloud.google.com/run/docs/configuring/services/environment-variables "Configure environment variables for services | Cloud Run"
[5]: https://docs.cloud.google.com/run/docs/container-contract "Container runtime contract | Cloud Run"
[6]: https://docs.cloud.google.com/run/docs/configuring/services/secrets "Configure secrets for services | Cloud Run"
