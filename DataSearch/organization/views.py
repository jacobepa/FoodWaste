from django.shortcuts import render
#
# View for managing the EPA organizational hierarchy
#
from django.shortcuts import render
import urllib.parse
from .models import *
from .forms import *

import urllib.parse
from organization.models import *
from projects.models import Project
from django.contrib.sessions.models import Session
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test



from django.views.generic import FormView, TemplateView
from constants.perms import apply_perms


# Create your views here.
class OfficeEditView(TemplateView):
    template_name = 'main/office.html'
    form_class = OfficeForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        user = request.user
        office_id = kwargs["office_id"]
        office = Office.objects.get(id=office_id)
        lab_list = Lab.objects.filter(office__id=office_id)
        is_editing = True

        form = self.form_class(instance=office, is_editable=is_editing)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        is_editing = False
        office_id = kwargs["office_id"]
        obj = Office.objects.get(id=office_id)
        lab_list = Lab.objects.filter(office__id=office_id)

        form = self.form_class(data=request.POST, files=request.FILES, instance=obj, is_editable=False)
        if form.is_valid():
            office = form.save(commit=False)
            if office.description == '':
                office.description = None
            if office.url == '':
                office.url = None

            office.save()
            form.save_m2m()

            success = True
            form = self.form_class(instance=office, is_editable=False)

        return render(request, self.template_name, locals())


class LabEditView(TemplateView):
    template_name = 'main/lab.html'
    form_class = LabForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        user = request.user
        lab_id = kwargs["lab_id"]
        lab = Lab.objects.get(id=lab_id)
        office = lab.office
        division_list = Division.objects.filter(lab__id=lab_id)
        is_editing = True

        form = self.form_class(instance=lab, is_editable=is_editing)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        lab_id = kwargs["lab_id"]
        lab = Lab.objects.get(id=lab_id)
        division_list = Division.objects.filter(lab__id=lab_id)
        office = lab.office
        is_editing = False

        form = self.form_class(data=request.POST, files=request.FILES, instance=lab, is_editable=is_editing)
        if form.is_valid():
            lab = form.save(commit=False)
            if lab.description == '':
                lab.description = None
            if lab.url == '':
                lab.url = None

            lab.save()
            form.save_m2m()

            success = True
            form = self.form_class(instance=lab, is_editable=False)


        return render(request, self.template_name, locals())


class DivisionEditView(TemplateView):
    template_name = 'main/division.html'
    form_class = DivisionForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        is_editing = True
        user = request.user
        division_id = kwargs["division_id"]
        division = Division.objects.get(id=division_id)
        lab = division.lab
        office = lab.office
        branch_list = Branch.objects.filter(division__id=division_id)

        form = self.form_class(instance=division, is_editable=is_editing)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        division_id = kwargs["division_id"]
        division = Division.objects.get(id=division_id)
        lab = division.lab
        office = lab.office
        branch_list = Branch.objects.filter(division__id=division_id)
        is_editing = False

        form = self.form_class(data=request.POST, instance=division, is_editable=is_editing)
        if form.is_valid():
            division = form.save(commit=False)
            if division.description == '':
                division.description = None
            if division.url == '':
                division.url = None

            division.save()
            form.save_m2m()

            success = True
            form = self.form_class(instance=division, is_editable=False)

        return render(request, self.template_name, locals())


class BranchEditView(TemplateView):
    template_name = 'main/branch.html'
    form_class = BranchForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        is_editing = True
        user = request.user
        branch_id = kwargs["branch_id"]
        branch = Branch.objects.get(id=branch_id)
        division = branch.division
        lab = branch.lab
        office = lab.office

        form = self.form_class(instance=branch, is_editable=is_editing, lab=lab)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        branch_id = kwargs["branch_id"]
        branch = Branch.objects.get(id=branch_id)
        is_editing = False

        form = self.form_class(data=request.POST, instance=branch, is_editable=is_editing)
        if form.is_valid():
            branch = form.save(commit=False)
            division = branch.division
            lab = division.lab
            branch.lab = lab
            office = lab.office
            if branch.description == '':
                branch.description = None
            if branch.url == '':
                branch.url = None

            branch.save()
            form.save_m2m()

            success = True
            form = self.form_class(instance=branch, is_editable=False, lab=lab)
        else:
            is_editing = True
            form = self.form_class(data=request.POST, files=request.FILES, instance=branch, is_editable=is_editing)
            # branch_id = request.POST["branch"]
            division = branch.division
            lab = division.lab
            branch.lab = lab
            office = lab.office


        return render(request, self.template_name, locals())

class LabToggleActiveView(TemplateView):
    template_name = 'main/office.html'
    form_class = OfficeForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        lab_id = kwargs["lab_id"]
        lab = Lab.objects.get(id=lab_id)
        office = lab.office
        profile = request.user.userprofile

        form = self.form_class(instance=lab, is_editable=False)

#        if profile.user_type == "SUPER":
        if profile.permissions == "ADMIN":
            if lab.is_active:
                lab.is_active = False
            else:
                lab.is_active = True

            lab.save()


        lab_list = Lab.objects.filter(office__id=office.id)

        return render(request, self.template_name, locals())

class DivisionToggleActiveView(TemplateView):
    template_name = 'main/lab.html'
    form_class = LabForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        division_id = kwargs["division_id"]
        division = Division.objects.get(id=division_id)
        lab = division.lab
        office = lab.office
        profile = request.user.userprofile

        form = self.form_class(instance=lab, is_editable=False)

#        if profile.user_type == "SUPER":
        if profile.permissions == "ADMIN":
            if division.is_active:
                division.is_active = False
            else:
                division.is_active = True

            division.save()


        division_list = Division.objects.filter(lab__id=lab.id)

        return render(request, self.template_name, locals())

class BranchToggleActiveView(TemplateView):
    template_name = 'main/division.html'
    form_class = DivisionForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        branch_id = kwargs["branch_id"]
        branch = Branch.objects.get(id=branch_id)
        division = branch.division
        lab = division.lab
        office = lab.office
        profile = request.user.userprofile

        form = self.form_class(instance=division, is_editable=False)

#        if profile.user_type == "SUPER":
        if profile.permissions == "ADMIN":
            if branch.is_active:
                branch.is_active = False
            else:
                branch.is_active = True

            branch.save()


        branch_list = Branch.objects.filter(division__id=division.id)

        return render(request, self.template_name, locals())


class OfficeCreateView(TemplateView):
    template_name = 'main/office.html'
    form_class = OfficeForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):

        form = self.form_class(is_editable=True)
        is_editing = True

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        is_editing = False

        form = self.form_class(data=request.POST,  is_editable=is_editing)
        if form.is_valid():
            office = form.save(commit=False)
            if office.description == '':
                office.description = None
            if office.url == '':
                office.url = None

            office.save()
            form.save_m2m()

            success = True
        else:
            is_editing = True
            form = self.form_class(data=request.POST, is_editable=is_editing)

        return render(request, self.template_name, locals())


class LabCreateView(TemplateView):
    template_name = 'main/lab.html'
    form_class = LabForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        office_id = kwargs['office_id']
        office = Office.objects.get(id=office_id)
        is_editing = True

        form = self.form_class(is_editable=is_editing, office=office)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        is_editing = False

        form = self.form_class(data=request.POST,  is_editable=is_editing)
        if form.is_valid():
            lab = form.save(commit=False)
            if lab.description == '':
                lab.description = None
            if lab.url == '':
                lab.url = None

            lab.save()
            form.save_m2m()
            print("Saved the lab")
            office = lab.office

            success = True
        else:
            is_editing = True
            form = self.form_class(data=request.POST, is_editable=is_editing)
            office_id = request.POST["office"]
            office = Office.objects.get(id=office_id)


        return render(request, self.template_name, locals())


class DivisionCreateView(TemplateView):
    template_name = 'main/division.html'
    form_class = DivisionForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        is_editing = True
        lab_id = kwargs["lab_id"]
        lab = Lab.objects.get(id=lab_id)
        office = lab.office

        form = self.form_class(is_editable=is_editing, lab=lab)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        is_editing = False

        form = self.form_class(data=request.POST,  is_editable=is_editing)
        if form.is_valid():
            division = form.save(commit=False)
            lab = division.lab
            division.office = division.lab.office
            if division.description == '':
                division.description = None
            if division.url == '':
                division.url = None

            division.save()
            form.save_m2m()

            success = True
        else:
            is_editing = True
            form = self.form_class(data=request.POST, is_editable=is_editing)
            lab_id = request.POST['lab']
            lab = Lab.objects.get(id=lab_id)
            office = lab.office

        return render(request, self.template_name, locals())


class BranchCreateView(TemplateView):
    template_name = 'main/branch.html'
    form_class = BranchForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        is_editing = True
        division_id = kwargs["division_id"]
        division = Division.objects.get(id=division_id)
        lab = division.lab
        office = lab.office

        form = self.form_class(is_editable=is_editing, division=division)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        is_editing = False

        form = self.form_class(data=request.POST,  is_editable=is_editing)
        if form.is_valid():
            branch = form.save(commit=False)
            division = branch.division
            lab = division.lab
            branch.lab = lab
            office = lab.office
            branch.office = office
            if branch.description == '':
                branch.description = None
            if branch.url == '':
                branch.url = None

            branch.save()
            form.save_m2m()

            success = True
        else:
            is_editing = True
            form = self.form_class(data=request.POST, is_editable=is_editing)
            division_id = request.POST["division"]
            division = Division.objects.get(id=division_id)
            lab = division.lab
            office = lab.office


        return render(request, self.template_name, locals())


class OfficeListView(TemplateView):
    template_name = 'main/list_offices.html'

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        office_list = Office.objects.all()

        return render(request, self.template_name, locals())


class OfficeDeleteView(TemplateView):
    template_name = 'main/list_offices.html'
    form_class = OfficeForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        office_id = kwargs["office_id"]
        office = Office.objects.get(id=office_id)
        profile = request.user.userprofile

#        if profile.user_type == "SUPER":
        if profile.permissions == "ADMIN":
            user_list = User.objects.filter(userprofile__office_id=office_id)
            project_list = Project.objects.filter(office__id=office_id)
            if user_list:
                error_message = 'Cannot delete office ' + office.abbreviation + ' because there are users associated with it.'
            elif project_list:
                error_message = 'Cannot delete office ' + office.abbreviation + ' because there are projects associated with it.'
            else:
                office.delete()
                office = None

        office_list = Office.objects.all()

        return render(request, self.template_name, locals())


class LabDeleteView(TemplateView):
    template_name = 'main/office.html'
    form_class = OfficeForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        lab_id = kwargs["lab_id"]
        lab = Lab.objects.get(id=lab_id)
        office = lab.office

        profile = request.user.userprofile

        form = self.form_class(instance=office, is_editable=False)

#        if profile.user_type == "SUPER":
        if profile.permissions == "ADMIN":
            user_list = User.objects.filter(userprofile__lab_id=lab_id)
            project_list = Project.objects.filter(lab__id=lab_id)
            if user_list:
                error_message = 'Cannot delete lab ' + lab.abbreviation + ' because there are users associated with it.'
            elif project_list:
                error_message = 'Cannot delete lab ' + lab.abbreviation + ' because there are projects associated with it.'
            else:
                print("DELETE LAB")
                lab.delete()
                lab = None

        lab_list = Lab.objects.filter(office__id=office.id)

        return render(request, self.template_name, locals())


class DivisionDeleteView(TemplateView):
    template_name = 'main/lab.html'
    form_class = LabForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        division_id = kwargs["division_id"]
        division = Division.objects.get(id=division_id)
        lab = division.lab
        office = lab.office
        profile = request.user.userprofile

        form = self.form_class(instance=lab, is_editable=False)

#        if profile.user_type == "SUPER":
        if profile.permissions == "ADMIN":
            user_list = User.objects.filter(userprofile__division_id=division_id)
            project_list = Project.objects.filter(division__id=division_id)
            if user_list:
                error_message = 'Cannot delete division ' + division.abbreviation + ' because there are users associated with it.'
            elif project_list:
                error_message = 'Cannot delete division ' + division.abbreviation + ' because there are projects associated with it.'
            else:
                division.delete()
                division = None

        division_list = Division.objects.filter(lab__id=lab.id)

        return render(request, self.template_name, locals())


class BranchDeleteView(TemplateView):
    template_name = 'main/division.html'
    form_class = DivisionForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        branch_id = kwargs["branch_id"]
        branch = Branch.objects.get(id=branch_id)
        division = branch.division
        lab = division.lab
        office = lab.office
        profile = request.user.userprofile

        form = self.form_class(instance=division, is_editable=False)

#        if profile.user_type == "SUPER":
        if profile.permissions == "ADMIN":
            user_list = User.objects.filter(userprofile__branch_id=branch_id)
            project_list = Project.objects.filter(branch__id=branch_id)
            if user_list:
                error_message = 'Cannot delete branch ' + branch.abbreviation + ' because there are users associated with it.'
            elif project_list:
                error_message = 'Cannot delete branch ' + branch.abbreviation + ' because there are projects associated with it.'
            else:
                branch.delete()
                branch = None



        branch_list = Branch.objects.filter(division__id=division.id)

        return render(request, self.template_name, locals())


class OfficeView(TemplateView):
    template_name = 'main/office.html'
    form_class = OfficeForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        office_id = kwargs["office_id"]
        office = Office.objects.get(id=office_id)
        lab_list = Lab.objects.filter(office__id=office_id)

        form = self.form_class(instance=office, is_editable=False)
        is_editing = False

        return render(request, self.template_name, locals())


class LabView(TemplateView):
    template_name = 'main/lab.html'
    form_class = LabForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        lab_id = kwargs["lab_id"]
        lab = Lab.objects.get(id=lab_id)
        office = lab.office
        division_list = Division.objects.filter(lab__id=lab_id)

        form = self.form_class(instance=lab, is_editable=False)

        return render(request, self.template_name, locals())


class DivisionView(TemplateView):
    template_name = 'main/division.html'
    form_class = DivisionForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        is_editing = False
        user = request.user
        division_id = kwargs["division_id"]
        division = Division.objects.get(id=division_id)
        branch_list = Branch.objects.filter(division__id=division_id)
        lab = division.lab
        office = lab.office

        form = self.form_class(instance=division, is_editable=is_editing)

        return render(request, self.template_name, locals())



class BranchView(TemplateView):
    template_name = 'main/branch.html'
    form_class = BranchForm

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        is_editing = False
        branch_id = kwargs["branch_id"]
        branch = Branch.objects.get(id=branch_id)
        division = branch.division
        lab = division.lab
        office = lab.office

        form = self.form_class(instance=branch, is_editable=is_editing)

        return render(request, self.template_name, locals())
