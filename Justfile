# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

sync:
    uv sync

lint:
    uv run ruff check .

fmt:
    uv run ruff format .

typecheck:
    uv run mypy src

test:
    uv run pytest

ci: lint typecheck test

dev:
    uv run uvicorn creditforge.main:app --reload

db-up:
    docker compose up -d postgres

db-down:
    docker compose down

migrate:
    uv run alembic upgrade head

makemigrations MESSAGE:
    uv run alembic revision --autogenerate -m "{{MESSAGE}}"
