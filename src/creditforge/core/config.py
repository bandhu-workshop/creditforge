# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    app_name: str = "creditforge"
    environment: str = "development"
    database_url: str = (
        "postgresql+asyncpg://creditforge:creditforge@localhost:5432/creditforge"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
