from decimal import *


from constants.models import *

from offices.models import *

from django.contrib.auth.models import User, AnonymousUser

from django.urls import reverse

from django.db import models
#from django.apps import get_model
from django.db.models import Q, Avg, Max, Min, Count, Sum


def get_lab_path(instance, filename):
	return '%s/labs/%s' %(instance.user.username, filename)
	
def get_isc_storage_path(instance, filename):
	return '%s/input_stream_compounds/%s' %(instance.user.username, filename)

class Lab(models.Model):
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	created_by = models.CharField(blank=True, null=True, max_length=255)
	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
	
	attachment = models.FileField(null=True, blank=True, upload_to=get_lab_path)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
	
	the_name = models.CharField(null=True, blank=True, max_length=255)
	abbreviation = models.CharField(null=True, blank=True, max_length=15)
	
	weblink = models.CharField(blank=True, null=True, max_length=255)
	ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)
	
	the_description = models.TextField(null=True, blank=True)
	designation_code = models.CharField(max_length=1, null=True, blank=True)

	class Meta:
		ordering = ['abbreviation',]
	
	def __str__(self):
		return self.abbreviation or ''