# test_entries.py (tests)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# Pylint skip this file because it wasn't created by EPA:
# pylint: skip-file
# Also disabling docstrings since this is not an EPA file
# pylint: disable=C0301,W0611,R0903,C0103,C0114,C0115,C0116

"""
emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil; coding: utf-8 -*-

ex: set sts=4 ts=4 sw=4 noet:
See COPYING file distributed along with the duecredit package for the
copyright and license terms.
"""


import random  # Could not find version that satisfies the requirement random.
import re  # Could not find a version that satisfies the requirement re.
import pickle  # Could not find version that satisfies the requirement pickle.
import os
import pytest
import duecredit.io

from six.moves import StringIO
from six import text_type
from ..collector import DueCreditCollector, Citation
from .test_collector import _sample_bibtex, _sample_doi, _sample_bibtex2
from ..entries import BibTeX, Doi, Text, Url


def test_comparison():
    """Not an EPA File, Skipping Doc."""
    assert Text("123") == Text("123")
    assert Text("123") != Text("124")
    assert Text("123", 'key') == Text("123", 'key')
    assert Text("123", 'key') != Text("123", 'key1')
    assert Text("123", 'key') != Text("124", 'key')

    assert Doi("123/1", 'key') == Doi("123/1", 'key')
    assert Url("http://123/1", 'key') == Url("http://123/1", 'key')


def test_sugaring_api():
    """Not an EPA File, Skipping Doc."""
    assert Url("http://1.com").url == "http://1.com"
    assert Doi("1.com").doi == "1.com"
