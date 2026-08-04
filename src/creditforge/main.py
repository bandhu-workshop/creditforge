# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from fastapi import FastAPI

from creditforge.api.health import router as health_router
from creditforge.api.v1.router import router as v1_router
from creditforge.core.config import get_settings
from creditforge.core.exceptions import register_exception_handlers
from creditforge.core.logging import setup_logging


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging()

    app = FastAPI(title=settings.app_name)
    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(v1_router)

    return app


app = create_app()
