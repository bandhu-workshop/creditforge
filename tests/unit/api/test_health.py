# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from fastapi import FastAPI
from fastapi.testclient import TestClient

from creditforge.api.health import router


def test_health_returns_ok():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
