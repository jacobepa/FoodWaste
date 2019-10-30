# test_utils.py (tests)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# Also disabling docstrings since this is not an EPA file
# pylint: disable=C0301,W0212,R0915,E1305,C0103,R0903,C0103,C0114,C0115,C0116

"""
emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-

ex: set sts=4 ts=4 sw=4 noet:
See COPYING file distributed along with the duecredit package for the
copyright and license terms. Originates from datalad package distributed
under MIT license.
"""

import sys
from ..utils import is_interactive


def test_is_interactive_crippled_stdout(monkeypatch):
    """Not an EPA File, Skipping Doc."""
    class MockedOut(object):
        """The one which has no isatty.        """

        def write(self, *args, **kwargs):
            """Not an EPA File, Skipping Doc."""

    class MockedIsaTTY(MockedOut):
        """Not an EPA File, Skipping Doc."""

        def isatty(self):
            """Not an EPA File, Skipping Doc."""
            return True

    for inout in ('in', 'out', 'err'):
        monkeypatch.setattr(sys, 'std%s' % inout, MockedOut())
        assert not is_interactive()

    # Just for paranoids.
    for inout in ('in', 'out', 'err'):
        monkeypatch.setattr(sys, 'std%s' % inout, MockedIsaTTY())
    assert is_interactive()
