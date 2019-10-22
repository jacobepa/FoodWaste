# models.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of models."""

from django.db import models
from django.utils import timezone
#from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class TrackingTool(models.Model):
    """Class representing an instance of Secondary / Existing Data Tracking Tool."""

    work = models.CharField(blank=False, null=False, max_length = 255)
    email = models.CharField(blank=False, null=False, max_length = 255)
    #phone = PhoneNumberField(blank=False, null=False)
    phone = models.CharField(blank=False, null=False, max_length = 32)
    search = models.CharField(blank=False, null=False, max_length = 255)
    article_title = models.CharField(blank=False, null=False, max_length = 255)
    citation = models.CharField(blank=False, null=False, max_length = 512)
    date_accessed = models.DateTimeField(blank=False, null=False, default=timezone.now)
    comments = models.CharField(blank=True, null=True, max_length = 512)
