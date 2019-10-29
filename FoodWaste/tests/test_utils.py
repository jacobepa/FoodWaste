# test_utils.py (tests)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# pylint: disable=C0301,R0903,R0201

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
    """TODO: Add function docstring."""
    class MockedOut(object):
        """The one which has no isatty.        """

        def write(self, *args, **kwargs):
            """TODO: Add function docstring."""

    class MockedIsaTTY(MockedOut):
        """Add docstring."""  # TODO add docstring.

        def isatty(self):
            """TODO: Add function docstring."""
            return True

    for inout in ('in', 'out', 'err'):
        monkeypatch.setattr(sys, 'std%s' % inout, MockedOut())
        assert not is_interactive()

    # Just for paranoids.
    for inout in ('in', 'out', 'err'):
        monkeypatch.setattr(sys, 'std%s' % inout, MockedIsaTTY())
    assert is_interactive()
