# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

import pytest

from creditforge.core.config import get_settings
from creditforge.db.session import get_engine


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    get_engine.cache_clear()
    yield
    get_settings.cache_clear()
    get_engine.cache_clear()
