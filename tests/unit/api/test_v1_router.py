# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from fastapi import FastAPI
from fastapi.testclient import TestClient

from creditforge.api.v1.router import router


def test_v1_router_mounts_under_expected_prefix():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    response = client.get("/api/v1/does-not-exist")

    assert response.status_code == 404
