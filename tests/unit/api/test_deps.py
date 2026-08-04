# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from typing import get_args

from creditforge.api.deps import DbSession
from creditforge.db.session import get_session


def test_db_session_depends_on_get_session():
    _, depends_marker = get_args(DbSession)

    assert depends_marker.dependency is get_session
