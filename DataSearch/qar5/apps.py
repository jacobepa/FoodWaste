# apps.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""
Application configuration objects store metadata for an application.

Some attributes can be configured in AppConfig subclasses. Others are set by
Django and read-only. This file is created to include any application
configuration for the app. Using this, you can configure some of the attributes
of the application.

Available functions:
It is the recommended best practice to place your application configuration
in the apps.py.
"""

from django.apps import AppConfig


class Qar5Config(AppConfig):
    """qar5 configuration."""

    name = 'qar5'
    verbose_name = "qar5"
    default_app_config = 'qar5.apps.Qar5Config'
