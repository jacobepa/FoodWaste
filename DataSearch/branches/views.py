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


from constants.models import *

from branches.models import *
from branches.forms import *

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

from django.shortcuts import get_object_or_404

from django.template import RequestContext, loader, Context

from django.views.decorators.cache import never_cache

@login_required
def index(request):
	user = request.user
	title = "Branches Main Page"
	objs = Branch.objects.all()
	return render(None, 'main/branches.html', locals())

########################################################################## Start Branch
		
@login_required
def create_branch(request):
	user = request.user
	title = "Create a New Branch"
	branches = Branch.objects.all()
	
	if request.method == "POST":
		form = BranchForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			if 'files' in request.FILES:
				files = request.FILES['files']
				files.user = user
					
			branch = form.save(commit=False)
			
			if branch.division is not None:
				branch.lab = branch.division.lab
				branch.immediate_office = branch.division.immediate_office
				branch.office = branch.division.office
				
			branch.user = user	
			branch.created_by = user.username
			branch.last_modified_by = user.username
			branch.save()
			
			url = '/branches/show/%s/' % str(branch.id)
			return HttpResponseRedirect(url)
	else:
		form = BranchForm()
	return render(request, 'create_office.html', locals())
	
@login_required
def edit_branch(request, obj_id):
	user = request.user
	
	title = "Update Branch"
	
	branch = Branch.objects.get(id=obj_id)
	branches = Branch.objects.all()
	
	if user.is_staff or user == branch.user:
		pass
	else:
		return render(request, 'no_edit.html', locals())
		

	if request.method == "POST":
		form = BranchForm(data=request.POST, files=request.FILES, instance=branch)
		if form.is_valid():			
			branch = form.save(commit=False)
				
			branch.last_modified_by = user.username
			branch.save()
			
			url = '/branches/show/%s/' % str(branch.id)
			return HttpResponseRedirect(url)
	else:
		form = BranchForm(instance=branch)
		
	return render(request, 'edit_office.html', locals())
	
@login_required
def delete_branch(request, obj_id):
	title = "Delete Branch"
	user = request.user
	branch = get_object_or_404(Branch, id=obj_id)
	
	if branch.user == user or user.is_staff:
		branch.delete()
		
	url = '/branches/list/'
	return HttpResponseRedirect(url)

@login_required	
def list_branches(request):
	user = request.user
	title = "Branch List"
	branches = Branch.objects.all().order_by('ordering')
	return render(request, 'list/list_branches.html', locals())
	
@login_required	
def list_labs_to_expand(request):
	user = request.user
	profile = user.userprofile
	title = "Project QA Tracking By Project Lead"
	lab = Lab.objects.get(profile.user_lab_one)
	divisions = Division.objects.filter(lab=lab)

	return render(request, 'list/list_branches_to_expand.html', locals())
	
@login_required	
def list_divisions_to_expand(request, obj_id):
	user = request.user
	title = "Project QA Tracking By Project Lead"
	lab = Lab.objects.get(id=obj_id)
	divisions = Division.objects.filter(lab=lab).order_by('abbreviation')

	return render(request, 'list/list_branches_to_expand.html', locals())
	
@login_required	
def list_branches_to_expand(request, obj_id):
	user = request.user
	title = "Project QA Tracking By Project Lead"
	division = Division.objects.get(id=obj_id)
	lab = division.lab
	divisions = Division.objects.filter(lab=lab).order_by('abbreviation')
	branches = Branch.objects.filter(division=division).order_by('abbreviation')

	return render(request, 'list/list_branches_to_expand.html', locals())
	
@login_required	
def list_branches_to_expand_two(request, obj_id):
	user = request.user
	title = "Project QA Tracking By Project Lead"
	obj = Branch.objects.get(id=obj_id)
	division = obj.division
	lab = division.lab
	divisions = Division.objects.filter(lab=lab).order_by('abbreviation')
	branches = Branch.objects.filter(division=division).order_by('abbreviation')
	projects = Project.objects.filter(Q(branch=obj)).order_by('project_status__the_name', 'person__last_name', 'qa_id')

	return render(request, 'list/list_branches_to_expand.html', locals())

@login_required	
@never_cache
def show_branch(request, obj_id):
	user = request.user
	
	obj = get_object_or_404(Branch, id=obj_id)
	title = "Show Branch"
	
	branches = Branch.objects.all()
	return render(request, 'show/show_branch.html', locals())		
	
def search_branch(request):
	title = "Search For Branch - With Results Shown"
	return render(request, 'main/search_branch.html', locals())

def result_search_branch(request):
	query = Q()
	query_show = ''
	x = int(0)
	y = int(0)
	title = "Search Branch - With Results Shown"
	
	if request is None:
		return Branch.objects.get(id=1)
	
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
		the_count = Branch.objects.filter(query).count()
		max_page_number = int(floor(the_count/50)) + 1
		if max_page_number <= pg:
			if the_count > count_per_page - 1:
				y = int(the_count)
				x = int(y - count_per_page)
			else:
				y = int(the_count)
				x = 0

		objs = Branch.objects.filter(query)[x:y]
	else:
		objs = ""
		
	return render(request, 'main/search_branch.html', locals())

####################################################################### End Branch
