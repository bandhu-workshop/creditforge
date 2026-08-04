# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from creditforge.core.config import Settings, get_settings


def test_settings_reads_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://u:p@host:5432/db")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.database_url == "postgresql+asyncpg://u:p@host:5432/db"


def test_settings_has_expected_defaults():
    settings = Settings()

    assert settings.app_name == "creditforge"
    assert settings.environment == "development"
