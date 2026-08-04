# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from fastapi.testclient import TestClient

from creditforge.main import create_app


def test_health_endpoint_reachable_through_app_factory():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_reachable_with_lifespan():
    with TestClient(create_app()) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
