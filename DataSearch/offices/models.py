from decimal import *


from constants.models import *

from django.contrib.auth.models import User, AnonymousUser

from django.urls import reverse

from django.db import models
#from django.apps import get_model, Q, Avg, Max, Min, Count, Sum

def get_office_path(instance, filename):
	return '%s/offices/%s' %(instance.user.username, filename)

class Office(models.Model):
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	created_by = models.CharField(blank=True, null=True, max_length=255)
	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
	
	attachment = models.FileField(null=True, blank=True, upload_to=get_office_path)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	
	the_name = models.CharField(null=True, blank=True, max_length=255)
	abbreviation = models.CharField(null=True, blank=True, max_length=15)
	
	weblink = models.CharField(blank=True, null=True, max_length=255)
	ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)
	
	the_description = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return self.the_name
