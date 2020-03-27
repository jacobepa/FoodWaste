from django.shortcuts import render
from xlwt import Workbook
import csv
import datetime
from . import models
import re
import json
import profile
import urllib.parse
from math import *
from decimal import *
getcontext().prec = 9


from constants.models import *

from divisions.models import *
from divisions.forms import *

from branches.models import *

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

from django.shortcuts import get_object_or_404

from django.template import RequestContext, loader, Context

from django.views.decorators.cache import never_cache

@login_required
def index(request):
	user = request.user
	title = "Divisions Main Page"
	objs = Division.objects.all()
	return render(None, 'main/divisions.html', locals())

########################################################################## Start Division
	
@login_required
def create_division(request):
	user = request.user
	title = "Create a New Division"
	divisions = Division.objects.all()
	
	if request.method == "POST":
		form = DivisionForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			division = form.save(commit=False)
			if division.immediate_office is not None:
				division.lab = division.immediate_office.lab
				division.office = division.immediate_office.office
				
			division.user = user	
			division.created_by = user.username
			division.last_modified_by = user.username
			division.save()
			
			url = '/divisions/show/%s/' % str(division.id)
			return HttpResponseRedirect(url)
	else:
		form = DivisionForm()
	return render(request, 'create_office.html', locals())
	
@login_required
def edit_division(request, obj_id):
	user = request.user
	
	title = "Update Division"
	
	division = Division.objects.get(id=obj_id)
	divisions = Division.objects.all()
	
	if user.is_staff or user == division.user:
		pass
	else:
		return render(request, 'no_edit.html', locals())
		
	if request.method == "POST":
		form = DivisionForm(data=request.POST, files=request.FILES, instance=division)
		if form.is_valid():			
			division = form.save(commit=False)
				
			division.last_modified_by = user.username
			division.save()
			
			url = '/divisions/show/%s/' % str(division.id)
			return HttpResponseRedirect(url)
	else:
		form = DivisionForm(instance=division)
		
	return render(request, 'edit_office.html', locals())
	
@login_required
def delete_division(request, obj_id):
	title = "Delete Division"
	user = request.user
	division = get_object_or_404(Division, id=obj_id)
	
	if division.user == user:
		division.delete()
		
	url = '/divisions/list/'
	return HttpResponseRedirect(url)

@login_required	
def list_divisions(request):
	user = request.user
	title = "Division List"
	divisions = Division.objects.all().order_by('abbreviation')
	return render(request, 'list/list_divisions.html', locals())


@login_required	
def list_divisions_to_expand_two(request, obj_id):
	user = request.user
	title = "Project QA Tracking By Project Lead"
	obj = Division.objects.get(id=obj_id)
	divisions = Division.objects.all().order_by('abbreviation')
	for division in divisions:
		division_branches = Branch.objects.filter(division=division).order_by('ordering')
	return render(request, 'list/list_divisions_to_expand.html', locals())

@login_required	
@never_cache
def show_division(request, obj_id):
	user = request.user
	
	obj = get_object_or_404(Division, id=obj_id)
	title = "Show Division"
	
	divisions = Division.objects.all()
	return render(request, 'show/show_division.html', locals())		
	
def search_division(request):
	title = "Search For Division - With Results Shown"
	return render(request, 'main/search_division.html', locals())

def result_search_division(request):
	query = Q()
	query_show = ''
	x = int(0)
	y = int(0)
	title = "Search Division - With Results Shown"
	
	if request is None:
		return Division.objects.get(id=1)
	
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
		the_count = Division.objects.filter(query).count()
		max_page_number = int(floor(the_count/50)) + 1
		if max_page_number <= pg:
			if the_count > count_per_page - 1:
				y = int(the_count)
				x = int(y - count_per_page)
			else:
				y = int(the_count)
				x = 0

		objs = Division.objects.filter(query)[x:y]
	else:
		objs = ""
		
	return render(request, 'main/search_division.html', locals())

####################################################################### End Division
