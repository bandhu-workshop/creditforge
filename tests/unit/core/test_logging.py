# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: Apache-2.0

import logging

from creditforge.core.logging import setup_logging


def test_setup_logging_sets_level_and_single_handler():
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)

    setup_logging(level="DEBUG")

    assert root.level == logging.DEBUG
    assert len(root.handlers) == 1


def test_setup_logging_is_idempotent():
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)

    setup_logging()
    setup_logging()

    assert len(root.handlers) == 1
