from decimal import *

from constants.models import *

from offices.models import *
from labs.models import *
from immediate_offices.models import *
from divisions.models import *

from django.contrib.auth.models import User, AnonymousUser

from django.urls import reverse

from django.db import models
#from django.apps import get_model
from django.db.models import Q, Avg, Max, Min, Count, Sum


def get_branch_path(instance, filename):
	return '%s/branches/%s' %(instance.user.username, filename)

class Branch(models.Model):
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	created_by = models.CharField(blank=True, null=True, max_length=255)
	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
	
	attachment = models.FileField(null=True, blank=True, upload_to=get_branch_path)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
	lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True, blank=True)
	immediate_office = models.ForeignKey(ImmediateOffice, on_delete=models.CASCADE, null=True, blank=True)
	division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
	
	the_name = models.CharField(null=True, blank=True, max_length=255)
	abbreviation = models.CharField(null=True, blank=True, max_length=15)
	
	weblink = models.CharField(blank=True, null=True, max_length=255)
	ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)
	
	the_description = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return self.division.abbreviation + " - " + self.abbreviation or ''
