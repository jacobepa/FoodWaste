from django.shortcuts import render
from xlwt import Workbook
import csv
import datetime
from . import models
import re
import json
import operator
import profile
import urllib.parse
from math import *
from decimal import *
getcontext().prec = 9

from audits.forms import *
from constants.models import *

from organization.models import *

from projects.models import *

from django.forms.models import modelformset_factory, inlineformset_factory

from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission

from django.conf import settings
from django.urls import reverse

from django.forms.models import modelformset_factory, inlineformset_factory

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#from django.apps import get_model
from django.db.models import Q, Avg, Max, Min, Count, Sum


from django.http import Http404, HttpResponseRedirect, HttpResponse

from django.shortcuts import render_to_response, get_object_or_404

from django.template import RequestContext, loader, Context

from django.views.decorators.cache import never_cache

@login_required
def index(request):
	user = request.user
	profile = user.userprofile
	title = "Audits Main Page"
	title = "Audits: Search or Create - Audits Are Now QA Activities But Will Be Separated Out Upon Launch"
	lab = Lab.objects.get(abbreviation=profile.lab)
	divisions = Division.objects.filter(lab=lab).order_by('abbreviation')
	return render(None, 'main/audits.html', locals())


########################################################################## Start Audit Type
	
@login_required
def create_audit_type(request):
	user = request.user
	title = "Create a New Audit Type"
	audit_types = AuditType.objects.all()
	
	if request.method == "POST":
		form = AuditTypeForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			audit_type = form.save(commit=False)
				
			audit_type.user = user	
			audit_type.created_by = user.username
			audit_type.last_modified_by = user.username
			audit_type.save()
			
			url = '/audits/type/show/%s/' % str(audit_type.id)
			return HttpResponseRedirect(url)
	else:
		form = AuditTypeForm()
	return render(request, 'create.html', locals())
	
@login_required
def edit_audit_type(request, obj_id):
	user = request.user
	
	title = "Update Audit Type"
	
	audit_type = AuditType.objects.get(id=obj_id)
	audit_types = AuditType.objects.all()
	
	if user.is_staff or user == audit_type.user:
		pass
	else:
		return render(request, 'no_edit.html', locals())

	if request.method == "POST":
		form = AuditTypeForm(data=request.POST, files=request.FILES, instance=audit_type)
		if form.is_valid():			
			audit_type = form.save(commit=False)
				
			audit_type.last_modified_by = user.username
			audit_type.save()
			
			url = '/audits/type/show/%s/' % str(audit_type.id)
			return HttpResponseRedirect(url)
	else:
		form = AuditTypeForm(instance=audit_type)
		
	return render(request, 'edit.html', locals())
	
@login_required
def delete_audit_type(request, obj_id):
	title = "Delete Audit Type"
	user = request.user
	audit_type = get_object_or_404(AuditType, id=obj_id)
	
	if audit_type.user == user:
		audit_type.delete()
		
	url = '/audits/type/list/'
	return HttpResponseRedirect(url)

@login_required	
def list_audit_types(request):
	user = request.user
	title = "Audit Type List"
	audit_types = AuditType.objects.all().order_by('the_name')
	return render(request, 'list/list_audit_types.html', locals())

@login_required	
@never_cache
def show_audit_type(request, obj_id):
	user = request.user
	
	obj = get_object_or_404(AuditType, id=obj_id)
	title = "Audit Type"

	return render(request, 'show/show.html', locals())		
	
def search_audit_type(request):
	title = "Search For Audit Type - With Results Shown"
	return render(request, 'main/search_audit_type.html', locals())

def result_search_audit_type(request):
	query = Q()
	query_show = ''
	x = int(0)
	y = int(0)
	title = "Search Audit Type- With Results Shown"
	
	if request is None:
		return AuditType.objects.get(id=1)
	
	if 'a' in request.GET:
		a = request.GET['a']
		if a:
			query = query & (Q(name__startswith=a))
			query_show = query_show + "User Compound Library Name = " + str(a) + " "
			
	if 'b' in request.GET:
		b = request.GET['b']
		if b:
			query = query & (Q(cas_number__startswith=b))
			query_show = query_show + "CAS Number = " + str(b) + " "
			
	if 'c' in request.GET:
		c = request.GET['c']
		if c:
			query = query & (Q(formula__startswith=c))
			query_show = query_show + "Molecular Formula = " + str(c) + " "
			
	count_per_page = 50
	
	if 'w' in request.GET:
		w = request.GET['w']
		if 'next' in request.GET:
			next = request.GET['next']
			page = int(page) + 1
			pg = int(page)
		if 'previous' in request.GET:
			previous = request.GET['previous']
			page = int(page) - 1
			if page == 0:
				page = 1
			pg = int(page)
		if 'start' in request.GET:
			start = request.GET['start']
			pg = int(page)
			
		if pg > 1:
			y = pg * count_per_page
			
			if y < count_per_page:
				x = 0
			else:
				x = y - count_per_page
		else:
			pg = 1
			y = count_per_page
			x = 0
	else:
		pg = 1
		y = count_per_page
		x = 0
	
	query = query & (Q(make_public="Y"))
	
	if query:
		the_count = AuditType.objects.filter(query).count()
		max_page_number = int(floor(the_count/50)) + 1
		if max_page_number <= pg:
			if the_count > count_per_page - 1:
				y = int(the_count)
				x = int(y - count_per_page)
			else:
				y = int(the_count)
				x = 0

		objs = AuditType.objects.filter(query)[x:y]
	else:
		objs = ""
		
	return render(request, 'main/search_audit_type.html', locals())

####################################################################### End Audit Type


########################################################################## Start Audit finding
	
@login_required
def create_audit_finding(request):
	user = request.user
	title = "Create a New Audit finding"
	audit_findings = AuditFinding.objects.all()
	
	if request.method == "POST":
		form = AuditFindingForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			audit_finding = form.save(commit=False)
				
			audit_finding.user = user	
			audit_finding.created_by = user.username
			audit_finding.last_modified_by = user.username
			audit_finding.save()
			
			url = '/audits/finding/show/%s/' % str(audit_finding.id)
			return HttpResponseRedirect(url)
	else:
		form = AuditFindingForm()
	return render(request, 'create.html', locals())
	
@login_required
def edit_audit_finding(request, obj_id):
	user = request.user
	
	title = "Update Audit finding"
	
	audit_finding = AuditFinding.objects.get(id=obj_id)
	audit_findings = AuditFinding.objects.all()
	
	if user.is_staff or user == audit_finding.user:
		pass
	else:
		return render(request, 'no_edit.html', locals())

	if request.method == "POST":
		form = AuditFindingForm(data=request.POST, files=request.FILES, instance=audit_finding)
		if form.is_valid():			
			audit_finding = form.save(commit=False)
				
			audit_finding.last_modified_by = user.username
			audit_finding.save()
			
			url = '/audits/finding/show/%s/' % str(audit_finding.id)
			return HttpResponseRedirect(url)
	else:
		form = AuditFindingForm(instance=audit_finding)
		
	return render(request, 'edit.html', locals())
	
@login_required
def delete_audit_finding(request, obj_id):
	title = "Delete Audit finding"
	user = request.user
	audit_finding = get_object_or_404(AuditFinding, id=obj_id)
	
	if audit_finding.user == user:
		audit_finding.delete()
		
	url = '/audits/finding/list/'
	return HttpResponseRedirect(url)

@login_required	
def list_audit_findings(request):
	user = request.user
	title = "Audit finding List"
	audit_findings = AuditFinding.objects.all().order_by('the_name')
	return render(request, 'list/list_audit_findings.html', locals())

@login_required	
@never_cache
def show_audit_finding(request, obj_id):
	user = request.user
	
	obj = get_object_or_404(AuditFinding, id=obj_id)
	title = "Audit finding"

	return render(request, 'show/show.html', locals())		
	
def search_audit_finding(request):
	title = "Search For Audit finding - With Results Shown"
	return render(request, 'main/search_audit_finding.html', locals())

def result_search_audit_finding(request):
	query = Q()
	query_show = ''
	x = int(0)
	y = int(0)
	title = "Search Audit finding- With Results Shown"
	
	if request is None:
		return AuditFinding.objects.get(id=1)
	
	if 'a' in request.GET:
		a = request.GET['a']
		if a:
			query = query & (Q(name__startswith=a))
			query_show = query_show + "User Compound Library Name = " + str(a) + " "
			
	if 'b' in request.GET:
		b = request.GET['b']
		if b:
			query = query & (Q(cas_number__startswith=b))
			query_show = query_show + "CAS Number = " + str(b) + " "
			
	if 'c' in request.GET:
		c = request.GET['c']
		if c:
			query = query & (Q(formula__startswith=c))
			query_show = query_show + "Molecular Formula = " + str(c) + " "
			
	count_per_page = 50
	
	if 'w' in request.GET:
		w = request.GET['w']
		if 'next' in request.GET:
			next = request.GET['next']
			page = int(page) + 1
			pg = int(page)
		if 'previous' in request.GET:
			previous = request.GET['previous']
			page = int(page) - 1
			if page == 0:
				page = 1
			pg = int(page)
		if 'start' in request.GET:
			start = request.GET['start']
			pg = int(page)
			
		if pg > 1:
			y = pg * count_per_page
			
			if y < count_per_page:
				x = 0
			else:
				x = y - count_per_page
		else:
			pg = 1
			y = count_per_page
			x = 0
	else:
		pg = 1
		y = count_per_page
		x = 0
	
	query = query & (Q(make_public="Y"))
	
	if query:
		the_count = AuditFinding.objects.filter(query).count()
		max_page_number = int(floor(the_count/50)) + 1
		if max_page_number <= pg:
			if the_count > count_per_page - 1:
				y = int(the_count)
				x = int(y - count_per_page)
			else:
				y = int(the_count)
				x = 0

		objs = AuditFinding.objects.filter(query)[x:y]
	else:
		objs = ""
		
	return render(request, 'main/search_audit_finding.html', locals())

####################################################################### End Audit finding
