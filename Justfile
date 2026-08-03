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
