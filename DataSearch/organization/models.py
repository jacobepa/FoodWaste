#
# Models representing the organizational structure of the EPA
#
# Offices - EPA offices (under the Office of the Administrator)
# Lab - Labs within an office
# Division - divisions within a lab
# Branch - branches within a division
#

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Office(models.Model):
    """
    EPA Office
    """
    office = models.CharField(blank=False, max_length=255)
    abbreviation = models.CharField(blank=False, max_length=32)
    url = models.CharField(blank=True, null=True, max_length=1024)
    description = models.TextField(null=True, blank=True)
    designation_code = models.CharField(blank=True, null=True, max_length=255)
    qams = models.ManyToManyField(User, related_name='office_qams', blank=True)

    def __str__(self):
        return self.abbreviation or ''


class Lab(models.Model):
    """
    EPA Lab (includes laboratories, centers, and offices within an Office object)
    """
    lab = models.CharField(blank=False, max_length=255)
    abbreviation = models.CharField(blank=False, max_length=32)
    url = models.CharField(blank=True, null=True, max_length=1024)
    description = models.TextField(null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, blank=False)
    designation_code = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.BooleanField(default=True)
    qams = models.ManyToManyField(User, related_name='lab_qams', blank=True)

    def __str__(self):
        return self.office.abbreviation + "-" + self.abbreviation or ''


class Division(models.Model):
    """
    EPA Division (within a Lab)
    """
    division = models.CharField(blank=False, max_length=255)
    abbreviation = models.CharField(blank=False, max_length=32)
    url = models.CharField(blank=True, null=True, max_length=1024)
    description = models.TextField(null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, blank=False)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, blank=False)
    is_active = models.BooleanField(default=True)
    qams = models.ManyToManyField(User, related_name='division_qams', blank=True)

    def __str__(self):
        return self.office.abbreviation + "-" + self.lab.abbreviation + "-" + self.abbreviation or ''


class Branch(models.Model):
    """
    EPA branch (within a division)
    """
    branch = models.CharField(blank=False, max_length=255)
    abbreviation = models.CharField(blank=False, max_length=32)
    url = models.CharField(blank=True, null=True, max_length=1024)
    description = models.TextField(null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, blank=False)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, blank=False)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, blank=False)
    is_active = models.BooleanField(default=True)
    qams = models.ManyToManyField(User, related_name='branch_qams', blank=True)

    def __str__(self):
        return (self.office.abbreviation + "-" + self.lab.abbreviation + "-" +
                self.division.abbreviation + "-" + self.abbreviation) or ''



