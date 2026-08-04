# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

# Domain routers (cards, recommendations, strategy, ...) are registered
# here with router.include_router(...) as they are built.
