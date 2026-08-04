# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from fastapi import FastAPI
from fastapi.testclient import TestClient

from creditforge.core.exceptions import NotFoundError, register_exception_handlers


def _build_test_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    def boom() -> None:
        raise NotFoundError("card not found")

    return app


def test_app_error_returns_mapped_status_and_detail():
    client = TestClient(_build_test_app())

    response = client.get("/boom")

    assert response.status_code == 404
    assert response.json() == {"detail": "card not found"}
