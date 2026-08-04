# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from creditforge.core.config import get_settings


@lru_cache
def get_engine() -> AsyncEngine:
    return create_async_engine(get_settings().database_url, echo=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        bind=get_engine(), expire_on_commit=False, class_=AsyncSession
    )
    async with session_factory() as session:
        yield session
