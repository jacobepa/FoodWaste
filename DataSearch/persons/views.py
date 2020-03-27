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

from accounts.models import *
from constants.models import *

from persons.models import *
from persons.forms import *

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

from django.shortcuts import render, render_to_response, get_object_or_404

from django.template import RequestContext, loader, Context

from django.views.decorators.cache import never_cache

@login_required
def index(request):
	user = request.user
	title = "Technical Leads Main Page"
	objs = Person.objects.all()
	return render(request, 'main/persons.html', {'user'})

########################################################################## Start Person
	
@login_required
def create_person(request):
	user = request.user
	title = "Create a New Technical Lead"
	persons = Person.objects.all()
	
	if request.method == "POST":
		form = PersonAdminForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			person = form.save(commit=False)
				
			person.user = user	
			person.created_by = user.username
			person.last_modified_by = user.username
			person.save()
			
			url = '/persons/show/%s/' % str(person.id)
			return HttpResponseRedirect(url)
	else:
		form = PersonAdminForm()
	return render(request, 'create.html', locals())
	
@login_required
def create_person_no_project(request):
	user = request.user
	title = "Create a New Technical Lead"
	persons = Person.objects.all()
	
	if request.method == "POST":
		form = PersonForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			person = form.save(commit=False)
				
			person.user = user	
			person.created_by = user.username
			person.last_modified_by = user.username
			person.save()
			
			url = '/persons/show/%s/' % str(person.id)
			return HttpResponseRedirect(url)
	else:
		form = PersonForm()
	return render(request, 'create.html', locals())
	
@login_required
def create_person_from_project(request, obj_id):
	user = request.user
	title = "Create a New Technical Lead"
	persons = Person.objects.all()
	project = Project.objects.get(id=obj_id)
	
	if request.method == "POST":
		form = PersonForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			person = form.save(commit=False)
				
			person.user = user	
			person.created_by = user.username
			person.last_modified_by = user.username
			person.save()
			
			url = '/projects/show/%s/' % str(project.id)
			return HttpResponseRedirect(url)
	else:
		form = PersonForm()
	return render(request, 'create.html', locals())
	
@login_required
def edit_person(request, obj_id):
	user = request.user
	
	title = "Update Technical Lead"
	
	person = Person.objects.get(id=obj_id)
	persons = Person.objects.all()
	
	if user.is_staff or user == person.user:
		pass
	else:
		return render(request, 'no_edit.html', locals())

	if request.method == "POST":
		form = PersonAdminForm(data=request.POST, files=request.FILES, instance=person)
		if form.is_valid():			
			person = form.save(commit=False)
				
			person.last_modified_by = user.username
			person.save()
			
			url = '/persons/show/%s/' % str(person.id)
			return HttpResponseRedirect(url)
	else:
		form = PersonAdminForm(instance=person)
		
	return render(request, 'edit.html', locals())

		
@login_required
def tie_user_to_person(request, obj_id):
	request_user = request.user
	title = "Update Technical Lead"
	
	person = Person.objects.get(id=obj_id)
	users = User.objects.all()
	
	if request.method == "POST":
		form = PersonTieForm(data=request.POST, files=request.FILES, instance=person)
		if form.is_valid():			
			person = form.save(commit=False)
				
			person.last_modified_by = request_user.username
			person.save()
			
			url = '/persons/show/%s/' % str(person.id)
			return HttpResponseRedirect(url)
	else:
		form = PersonTieForm(instance=person)
		
	return render(request, 'edit.html', locals())

@login_required	
def list_persons(request):
	user = request.user
	title = "Technical Lead List"
	persons = Person.objects.all().order_by('last_name', 'first_name')
	return render(request, 'list/list_persons.html', locals())
	
@login_required	
def list_persons_to_expand(request):
	user = request.user
	title = "Technical Lead List"
	persons = Person.objects.all().order_by('ordering')
	return render(request, 'list/list_persons.html', locals())

@login_required	
@never_cache
def show_person(request, obj_id):
	user = request.user
	
	obj = get_object_or_404(Person, id=obj_id)
	title = "Show Technical Lead"
	
	projects = Project.objects.filter(person_id=obj.id)
	reviews = ProjectLog.objects.filter(reviewer_id=obj.id)
	qlogs = ProjectLog.objects.filter(technical_lead_id=obj.id)
	return render(request, 'show/show_person.html', locals())		
	
def search_person(request):
	title = "Search For Technical Lead - With Results Shown"
	return render(request, 'main/search_person.html', locals())

def result_search_person(request):
	query = Q()
	query_show = ''
	x = int(0)
	y = int(0)
	title = "Search Technical Lead - With Results Shown"
	
	if request is None:
		return Person.objects.get(id=1)
	
	if 'a' in request.GET:
		a = request.GET['a']
		if a:
			query = query & (Q(last_name__startswith=a))
			query_show = query_show + "Last Name = " + str(a) + " "
			
	if 'b' in request.GET:
		b = request.GET['b']
		if b:
			query = query & (Q(first_name__startswith=b))
			query_show = query_show + "First Name = " + str(b) + " "

	objs = Person.objects.filter(query)
		
	return render(request, 'main/search_person.html', locals())

####################################################################### End Person


########################################################################## Start PersonStatus
	
@login_required
def create_person_status(request):
	user = request.user
	title = "Create a New Technical Lead Status"
	person_statuses = PersonStatus.objects.all()
	
	if request.method == "POST":
		form = PersonStatusForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			person_status = form.save(commit=False)
				
			person_status.user = user	
			person_status.created_by = user.username
			person_status.last_modified_by = user.username
			person_status.save()
			
			url = '/persons/person_status/show/%s/' % str(person_status.id)
			return HttpResponseRedirect(url)
	else:
		form = PersonStatusForm()
	return render(request, 'create_office.html', locals())
	
@login_required
def edit_person_status(request, obj_id):
	user = request.user
	
	title = "Update Technical Lead Status"
	
	person_status = PersonStatus.objects.get(id=obj_id)
	person_statuses = PersonStatus.objects.all()
	
	if user.is_staff or user == person_status.user:
		pass
	else:
		return render(request, 'no_edit.html', locals())
		
	if person_status.user == user:
		if request.method == "POST":
			form = PersonStatusForm(data=request.POST, files=request.FILES, instance=person_status)
			if form.is_valid():			
				person_status = form.save(commit=False)
				
				person_status.last_modified_by = user.username
				person_status.save()
			
				url = '/persons/person_status/show/%s/' % str(person_status.id)
				return HttpResponseRedirect(url)
		else:
			form = PersonStatusForm(instance=person_status)
	else:
		url = '/accounts/not_authorized/'
		
	return render(request, 'edit_office.html', locals())
	
@login_required
def delete_person_status(request, obj_id):
	title = "Delete Technical Lead Status"
	user = request.user
	person_status = get_object_or_404(PersonStatus, id=obj_id)
	
	if person_status.user == user:
		person_status.delete()
		
	url = '/persons/person_status/list/'
	return HttpResponseRedirect(url)

@login_required	
def list_person_statuses(request):
	user = request.user
	title = "Technical Lead Status List"
	person_statuses = PersonStatus.objects.all().order_by('the_name')
	return render(request, 'list/list_person_statuses.html', locals())

@login_required	
@never_cache
def show_person_status(request, obj_id):
	user = request.user
	
	obj = get_object_or_404(PersonStatus, id=obj_id)
	title = "Show Technical Lead Status"
	
	person_statuses = PersonStatus.objects.all()
	return render(request, 'show/show_person_status.html', locals())		
	
def search_person_status(request):
	title = "Search For Technical Lead Status - With Results Shown"
	return render(request, 'main/search_person_status.html', locals())

def result_search_person_status(request):
	query = Q()
	query_show = ''
	x = int(0)
	y = int(0)
	title = "Search Technical Lead Status- With Results Shown"
	
	if request is None:
		return PersonStatus.objects.get(id=1)
	
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
		the_count = PersonStatus.objects.filter(query).count()
		max_page_number = int(floor(the_count/50)) + 1
		if max_page_number <= pg:
			if the_count > count_per_page - 1:
				y = int(the_count)
				x = int(y - count_per_page)
			else:
				y = int(the_count)
				x = 0

		objs = PersonStatus.objects.filter(query)[x:y]
	else:
		objs = ""
		
	return render(request, 'main/search_person_status.html', locals())

####################################################################### End PersonStatus
