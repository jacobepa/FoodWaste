# views.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""Definition of qar5 views."""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from qar5.forms import QappForm, QappApprovalForm, QappLeadForm
from qar5.models import Qapp, QappApproval, QappLead

class QappCreate(LoginRequiredMixin, CreateView):
    """Class for creating new QAPPs (Quality Assurance Project Plans)"""
    model = Qapp
    template_name = 'SectionA/qapp_create.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new QAPP."""
        return render(
            request, 'SectionA/qapp_create.html',
            {'form': QappForm(),
            'project_lead_class': QappLeadForm})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new QAPP form filled out."""
        form = QappForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            return HttpResponseRedirect('/qar5/approval/create?qapp_id=%d' % obj.id)
            #return HttpResponseRedirect('/qar5/detail/%d/' % obj.id)

        return render(request, 'qar5/SectionA/qapp_create.html', {'form': form})


class QappDetail(LoginRequiredMixin, DetailView):
    """Class for viewing an existing (newly created) QAPP"""
    model = Qapp
    template_name = 'SectionA/qapp_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_leads_list'] = QappLead.objects.filter(
            qapp=context['object'])
        context['project_approval'] =  QappApproval.objects.get(
            qapp=context['object'])
        return context


class ProjectLeadCreate(LoginRequiredMixin, CreateView):
    """Class for creating new QAPP Project Lead"""
    model = QappLead
    template_name = 'SectionA/project_lead_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new QAPP."""
        qapp_id = request.GET.get('qapp_id', 0)
        qapp = Qapp.objects.get(id=qapp_id)
        form = QappLeadForm({'qapp': qapp})
        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Project Lead form filled out."""
        form = QappLeadForm(request.POST)
        qapp_id = request.POST.get('qapp_id', 0)
        if form.is_valid():
            obj = form.save(commit=True)
            return HttpResponseRedirect(
                '/qar5/detail/%s/' % qapp_id)
        #return HttpResponseRedirect('/qar5/create/')
        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)


class ProjectApprovalCreate(LoginRequiredMixin, CreateView):
    """
    Create the base approval page with no signatures.
    Approval signatures will be added after the title and number.
    """
    template_name = 'SectionA/qapp_approval_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new QAPP."""
        qapp_id = request.GET.get('qapp_id', 0)
        qapp = Qapp.objects.get(id=qapp_id)
        form = QappApprovalForm({'qapp': qapp})
        ctx = {'form': form, 'qapp_id': qapp_id}

        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Project Lead form filled out."""
        form = QappApprovalForm(request.POST)
        qapp_id = form.data.get('qapp', '')
        if form.is_valid():
            obj = form.save(commit=True)
            return HttpResponseRedirect('/qar5/detail/%s/' % qapp_id)

        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)
    
