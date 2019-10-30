# test_cmdline.py (tests)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# Also disabling docstrings since this is not an EPA file
# pylint: disable=C0301,W0611,R0903,C0103,C0114,C0115,C0116

"""
emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-

ex: set sts=4 ts=4 sw=4 noet:
See COPYING file distributed along with the duecredit package for the
copyright and license terms.
"""


import sys
import pytest

from six.moves import StringIO
from .. import __version__
from ..cmdline import main


def test_import():
    """Not an EPA File, Skipping Doc."""
    import duecredit.cmdline
    import duecredit.cmdline.main


def test_main_help(monkeypatch):
    """Patch stdout."""
    fakestdout = StringIO()
    monkeypatch.setattr(sys, "stdout", fakestdout)

    pytest.raises(SystemExit, main.main, ['--help'])
    assert fakestdout.getvalue().lstrip().startswith("Usage: ")


def test_main_version(monkeypatch):
    """Patch stdout or stderr for different Python versions - catching both."""
    fakestdout = StringIO()
    fakeout = 'std' + ('err' if sys.version_info < (3, 4) else 'out')
    monkeypatch.setattr(sys, fakeout, fakestdout)

    pytest.raises(SystemExit, main.main, ['--version'])
    assert (fakestdout.getvalue()).split('\n')[0] == "duecredit %s" % __version__


# Smoke test the cmd_summary.
# TODO: carry sample .duecredit.p, point to that file, monkeypatch
# TextOutput and BibTeXOutput .dumps.
def test_smoke_cmd_summary():
    """Not an EPA File, Skipping Doc."""
    main.main(['summary'])


def test_cmd_test():
    """Test the not implemented cmd_test."""
    pytest.raises(SystemExit, main.main, ['test'])
