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

from offices.forms import *
from offices.models import *

from labs.models import *

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
	title = "Offices Main Page"
	objs = Office.objects.all()
	return render(None, 'main/offices.html', locals())
	
########################################################################## Start Office
	
@login_required
def create_office(request):
	user = request.user
	title = "Create a New Office"
	offices = Office.objects.all()
	
	if request.method == "POST":
		form = OfficeForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			office = form.save(commit=False)
				
			office.user = user	
			office.created_by = user.username
			office.last_modified_by = user.username
			office.save()
			
			url = '/offices/show/%s/' % str(office.id)
			return HttpResponseRedirect(url)
	else:
		form = OfficeForm()
	return render(request, 'create_office.html', locals())
	
@login_required
def edit_office(request, obj_id):
	user = request.user
	
	title = "Update Office"
	
	office = Office.objects.get(id=obj_id)
	offices = Office.objects.all()
	
	if user.is_staff or user == office.user:
		pass
	else:
		return render(request, 'no_edit.html', locals())
		
	if office.user == user:
		if request.method == "POST":
			form = OfficeForm(data=request.POST, files=request.FILES, instance=office)
			if form.is_valid():			
				office = form.save(commit=False)
				
				office.last_modified_by = user.username
				office.save()
			
				url = '/offices/show/%s/' % str(office.id)
				return HttpResponseRedirect(url)
		else:
			form = OfficeForm(instance=office)
	else:
		url = '/accounts/not_authorized/'
		
	return render(request, 'edit_office.html', locals())
	
@login_required
def delete_office(request, obj_id):
	title = "Delete Office"
	user = request.user
	office = get_object_or_404(Office, id=obj_id)
	
	if office.user == user:
		office.delete()
		
	url = '/offices/list/'
	return HttpResponseRedirect(url)

@login_required	
def list_offices(request):
	user = request.user
	title = "Office List"
	offices = Office.objects.all().order_by('ordering')
	return render(request, 'list/list_offices.html', locals())

@login_required	
@never_cache
def show_office(request, obj_id):
	user = request.user
	
	obj = get_object_or_404(Office, id=obj_id)
	title = "Show Office"
	
	offices = Office.objects.all().order_by('ordering')
	labs = Lab.objects.filter(office=obj).order_by('ordering')
	return render(request, 'show/show_office.html', locals())		
	
def search_office(request):
	title = "Search For Office - With Results Shown"
	return render(request, 'main/search_office.html', locals())

def result_search_office(request):
	query = Q()
	query_show = ''
	x = int(0)
	y = int(0)
	title = "Search Office - With Results Shown"
	
	if request is None:
		return Office.objects.get(id=1)
	
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
		the_count = Office.objects.filter(query).count()
		max_page_number = int(floor(the_count/50)) + 1
		if max_page_number <= pg:
			if the_count > count_per_page - 1:
				y = int(the_count)
				x = int(y - count_per_page)
			else:
				y = int(the_count)
				x = 0

		objs = Office.objects.filter(query)[x:y]
	else:
		objs = ""
		
	return render(request, 'main/search_office.html', locals())

####################################################################### End Office
