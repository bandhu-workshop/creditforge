# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "creditforge.models",
        "creditforge.schemas",
        "creditforge.services",
        "creditforge.ai",
        "creditforge.ai.agents",
        "creditforge.ai.tools",
    ],
)
def test_layer_package_imports(module_name: str) -> None:
    importlib.import_module(module_name)
