from decimal import *

from divisions.models import *
from branches.models import *

from django.urls import reverse

#from django.apps import get_model
from django.db.models import Q, Avg, Max, Min, Count, Sum

from django.db import models

class AuditType(models.Model):
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	created_by = models.CharField(blank=True, null=True, max_length=255)
	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
		
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	
	the_name = models.CharField(null=True, blank=True, max_length=255)
	abbreviation = models.CharField(null=True, blank=True, max_length=15)
	is_active = models.CharField(null=True, blank=True, max_length=4, choices=YN_CHOICES)
	
	weblink = models.CharField(blank=True, null=True, max_length=255)
	ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)
	
	the_description = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return self.the_name or ''
		
