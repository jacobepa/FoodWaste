
import sys
import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_save
from decimal import *

from constants.models import *
from organization.models import *



def get_profile_photo_storage_path(instance, filename):
    return 'profiles/%s/%s' %(instance.user.id, filename)

def get_contact_request_path(instance, filename):
    return 'contact_requests/%s' %(filename)

class UserProfile(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    attachment = models.FileField(null=True, blank=True, upload_to=get_profile_photo_storage_path)

    user_type = models.CharField(blank=True, null=True, max_length=45, choices=USER_TYPE_CHOICES)
    code_kept = models.CharField(blank=True, null=True, max_length=30)
    telephone = models.CharField(blank=True, null=True, max_length=30)
    telephone_extension = models.CharField(blank=True, null=True, max_length=30)
    # obsolete, but keeping until live data is migrated
    user_lab_one = models.CharField(blank=True, null=True, max_length=45)
    user_division_one = models.CharField(blank=True, null=True, max_length=45)
    user_branch_one = models.CharField(blank=True, null=True, max_length=45)

    mail_to_name = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    mail_to_address = models.CharField(blank=True, null=True, max_length=255)
    mail_to_city = models.CharField(blank=True, null=True, max_length=255)
    mail_to_state = models.CharField(blank=True, null=True, max_length=255)
    mail_to_zipcode = models.CharField(blank=True, null=True, max_length=255)
    mail_to_mailstop = models.CharField(blank=True, null=True, max_length=255)
    mail_to_note = models.CharField(blank=True, null=True, max_length=255)

    company = models.CharField(blank=True, null=True, max_length=255)

    email_address_epa = models.CharField(blank=True, null=True, max_length=255)
    email_address_other = models.CharField(blank=True, null=True, max_length=255)

    is_reviewer = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
    is_technical_lead = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
    can_edit = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
    can_create_users = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)

    display_in_dropdowns = models.CharField(default='Y', max_length=4, choices=YN_CHOICES, db_index=True)
    date_epa_separation = models.DateField(null=True, blank=True, db_index=True)

    permissions = models.CharField(blank=False, null=False, max_length=45, choices=PERMISSION_CHOICES, default="READER")

    def __str__(self):
        the_name = self.user.username
        full_name = self.user.first_name + self.user.last_name
        return the_name or ''

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    def r_name(self):
        return '%s, %s' % (self.user.last_name, self.user.first_name)

class RequestSubject(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    the_name = models.CharField(null=True, blank=True, max_length=255)
    email_address = models.CharField(null=True, blank=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)

    def __str__(self):
        return self.the_name or ''

class ContactRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, upload_to=get_contact_request_path)

    request_subject = models.ForeignKey(RequestSubject, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(null=True, blank=True, max_length=255)
    email_address = models.CharField(null=True, blank=True, max_length=255)

    greenscope_response = models.CharField(null=True, blank=True, max_length=255)
    response_date = models.DateField(null=True, blank=True)

    the_description = models.TextField(null=True, blank=True)

class UserDropdownInfo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(null=True, blank=True, max_length=30)
    last_name = models.CharField(null=True, blank=True, max_length=30)
    email = models.CharField(null=True, blank=True, max_length=254)
    # display_value = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'app_user_dropdown'
