# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from creditforge.db.session import get_engine, get_session


def test_get_engine_returns_async_engine():
    engine = get_engine()

    assert isinstance(engine, AsyncEngine)


async def test_get_session_yields_async_session():
    session_gen = get_session()
    session = await anext(session_gen)
    try:
        assert isinstance(session, AsyncSession)
    finally:
        await session_gen.aclose()
