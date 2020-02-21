# views.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""Definition of qar5 views."""

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, \
    TemplateView, UpdateView
from constants.qar5 import SECTION_A_INFO, SECTION_B_INFO, \
    SECTION_C_DEFAULTS, SECTION_D_INFO, SECTION_E_INFO, SECTION_F_INFO
from DataSearch.settings import DATETIME_FORMAT
from qar5.forms import QappForm, QappApprovalForm, QappLeadForm, \
    QappApprovalSignatureForm, SectionAForm, SectionBForm, SectionDForm, \
    RevisionForm, ReferencesForm
from qar5.models import Qapp, QappApproval, QappLead, QappApprovalSignature, \
    SectionA, SectionB, SectionBType, SectionC, SectionD, Revision, References

class QappList(LoginRequiredMixin, ListView):
    """Class for listing this user's (or all if admin) QAR5 objects."""
    model = Qapp
    template_name = 'qapp_list.html'
    context_object_name = 'qapp_list'

    def get_queryset(self):
        """
        Custom method override to send data to the template. Specifically,
        we want to send only data that belongs (prepared_by) the user.
        """
        user = self.request.user
        if user.is_superuser:
            return Qapp.objects.all()
        else:
            return Qapp.objects.filter(prepared_by=user)
    

class QappEdit(LoginRequiredMixin, UpdateView):
    """View for editing the details of an existing Qapp instance."""

    model = Qapp
    form_class = QappForm
    template_name = 'qapp_edit.html'

    def form_valid(self, form):
        """Qapp Edit Form validation and redirect."""
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/qar5/detail/' + str(self.object.id))


class QappCreate(LoginRequiredMixin, CreateView):
    """Class for creating new QAPPs (Quality Assurance Project Plans)."""

    model = Qapp
    template_name = 'qapp_create.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new QAPP."""
        return render(
            request, 'qapp_create.html',
            {'form': QappForm(),
            'project_lead_class': QappLeadForm})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new QAPP form filled out."""
        form = QappForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # Assign current user as the prepared_by
            obj.prepared_by = request.user
            obj.save()
            return HttpResponseRedirect('/qar5/approval/create?qapp_id=%d' % obj.id)

        return render(request, 'qapp_create.html', {'form': form})


class QappDetail(LoginRequiredMixin, DetailView):
    """Class for viewing an existing (newly created) QAPP."""

    model = Qapp
    template_name = 'qapp_detail.html'

    def get_context_data(self, **kwargs):
        """Add method docstring."""  # TODO add docstring.
        context = super().get_context_data(**kwargs)
        context['project_leads_list'] = QappLead.objects.filter(
            qapp=context['object'])
        context['project_approval'] =  QappApproval.objects.get(
            qapp=context['object'])
        context['project_approval_signatures'] = \
            QappApprovalSignature.objects.filter(
                qapp_approval=context['project_approval'])
        context['SECTION_A_INFO'] = SECTION_A_INFO
        return context


class ProjectLeadCreate(LoginRequiredMixin, CreateView):
    """Class for creating new QAPP Project Lead."""

    model = QappLead
    template_name = 'SectionA/project_lead_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new Project Lead."""
        qapp_id = request.GET.get('qapp_id', 0)
        qapp = Qapp.objects.get(id=qapp_id)
        form = QappLeadForm({'qapp': qapp})
        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Project Lead form filled out."""
        form = QappLeadForm(request.POST)
        qapp_id = request.POST.get('qapp', None)
        if form.is_valid():
            obj = form.save(commit=True)
            return HttpResponseRedirect(
                '/qar5/detail/%s' % qapp_id)
        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)


class ProjectApprovalCreate(LoginRequiredMixin, CreateView):
    """
    Create the base approval page with no signatures.

    Approval signatures will be added after the title and number.
    """

    template_name = 'qapp_approval_create.html'

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
            return HttpResponseRedirect('/qar5/detail/%s' % qapp_id)

        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)


class ProjectApprovalSignatureCreate(LoginRequiredMixin, CreateView):
    """Class for creating new QAPP Project Approval Signatures."""

    model = QappApprovalSignature
    template_name = 'SectionA/project_approval_signature_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new Approval Signature."""
        qapp_id = request.GET.get('qapp_id', 0)
        qapp = Qapp.objects.get(id=qapp_id)
        qapp_approval = QappApproval.objects.get(qapp=qapp)
        form = QappApprovalSignatureForm({'qapp': qapp, 'qapp_approval': qapp_approval})
        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Project Lead form filled out."""
        form = QappApprovalSignatureForm(request.POST)
        approval_id = request.POST.get('qapp_approval', None)
        approval = QappApproval.objects.get(id=approval_id)
        qapp_id = approval.qapp.id

        if form.is_valid():
            obj = form.save(commit=True)
            return HttpResponseRedirect(
                '/qar5/detail/%s' % qapp_id)
        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)



class SectionAView(LoginRequiredMixin, TemplateView):
    """Class for processing QAPP Section A (A.3 and later) information."""

    template_name = 'SectionA/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return the index page for QAR5 Section A (A.3 and later)."""
        assert isinstance(request, HttpRequest)
        qapp_id = request.GET.get('qapp_id', None)
        qapp = Qapp.objects.get(id=qapp_id)
        existing_section_a = SectionA.objects.filter(qapp=qapp).first()

        if existing_section_a:
            form = SectionAForm(instance=existing_section_a)

        else:
            form = SectionAForm({'qapp': qapp,
                                 'a3': SECTION_A_INFO['a3'],
                                 'a9': SECTION_A_INFO['a9']})

        return render(request, self.template_name,
                      {'title': 'QAR5 Section A', 'qapp_id': qapp_id,
                       'SECTION_A_INFO': SECTION_A_INFO, 'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a SectionA form filled out."""
        ctx = {'qapp_id': request.GET.get('qapp_id', None),
               'SECTION_A_INFO': SECTION_A_INFO, 'title': 'QAR5 Section A'}

        qapp = Qapp.objects.get(id=ctx['qapp_id'])
        existing_section_a = SectionA.objects.filter(qapp=qapp).first()

        # Update if existing, otherwise insert new:
        if existing_section_a:
            ctx['form'] = SectionAForm(instance=existing_section_a,
                                       data=request.POST)
        else:
            ctx['form'] = SectionAForm(request.POST)

        if ctx['form'].is_valid():
            ctx['obj'] = ctx['form'].save(commit=True)
            ctx['save_success'] = 'Successfully Saved Changes!'

        return render(request, self.template_name, ctx)


class SectionBView(LoginRequiredMixin, TemplateView):
    """Class for processing QAPP Section B information."""

    template_name = 'SectionB/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return the index page for QAR5 Section B."""
        assert isinstance(request, HttpRequest)
        qapp_id = request.GET.get('qapp_id', None)
        qapp = Qapp.objects.get(id=qapp_id)
        sectiona = SectionA.objects.get(qapp_id=qapp_id)
        sectionb_type_id = sectiona.sectionb_type_id
        sectionb_type = SectionBType.objects.get(id=sectionb_type_id)
        
        existing_section_b = SectionB.objects.filter(qapp=qapp).first()

        if existing_section_b:
            form = SectionBForm(instance=existing_section_b)

        else:
            form = SectionBForm({'qapp': qapp})

        # TODO pass in SectionB Form
        return render(request, self.template_name,
                      {'title': 'QAR5 Section B', 'qapp_id': qapp_id,
                       'SECTION_B_INFO': SECTION_B_INFO, 'form': form,
                       'sectionb_type': sectionb_type})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a SectionB form filled out."""
        ctx = {'qapp_id': request.GET.get('qapp_id', None),
               'SECTION_B_INFO': SECTION_B_INFO, 'title': 'QAR5 Section B'}

        qapp = Qapp.objects.get(id=ctx['qapp_id'])
        existing_section_b = SectionB.objects.filter(qapp=qapp).first()

        # Update if existing, otherwise insert new:
        if existing_section_b:
            ctx['form'] = SectionBForm(instance=existing_section_b,
                                       data=request.POST)
        else:
            ctx['form'] = SectionBForm(request.POST)

        if ctx['form'].is_valid():
            ctx['obj'] = ctx['form'].save(commit=True)
            ctx['save_success'] = 'Successfully Saved Changes!'

        return render(request, self.template_name, ctx)

    
class SectionCView(LoginRequiredMixin, TemplateView):
    """Class for processing QAPP Section C information."""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return the index page for QAR5 Section C."""
        assert isinstance(request, HttpRequest)
        qapp_id = request.GET.get('qapp_id', None)
        return render(request, 'SectionC/index.html',
                      {'title': 'QAR5 Section C', 'qapp_id': qapp_id,
                       'SECTION_C_DEFAULTS': SECTION_C_DEFAULTS})


class SectionDView(LoginRequiredMixin, TemplateView):
    """Class for processing QAPP Section D information."""

    template_name = 'SectionD/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return the index page for QAR5 Section D."""
        assert isinstance(request, HttpRequest)
        qapp_id = request.GET.get('qapp_id', None)
        qapp = Qapp.objects.get(id=qapp_id)
        existing_section_d = SectionD.objects.filter(qapp=qapp).first()

        if existing_section_d:
            form = SectionDForm(instance=existing_section_d)

        else:
            form = SectionDForm({'qapp': qapp})

        return render(request, self.template_name,
                      {'title': 'QAR5 Section D', 'qapp_id': qapp_id,
                       'SECTION_D_INFO': SECTION_D_INFO,
                       'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a SectionD form filled out."""
        ctx = {'qapp_id': request.GET.get('qapp_id', None),
               'SECTION_D_INFO': SECTION_D_INFO, 'title': 'QAR5 Section D'}

        qapp = Qapp.objects.get(id=ctx['qapp_id'])
        existing_section_d = SectionD.objects.filter(qapp=qapp).first()

        # Update if existing, otherwise insert new:
        if existing_section_d:
            ctx['form'] = SectionDForm(instance=existing_section_d,
                                       data=request.POST)
        else:
            ctx['form'] = SectionDForm(request.POST)

        if ctx['form'].is_valid():
            ctx['obj'] = ctx['form'].save(commit=True)
            ctx['save_success'] = 'Successfully Saved Changes!'

        return render(request, self.template_name, ctx)


class SectionEView(LoginRequiredMixin, TemplateView):
    """Class for processing QAPP Section E information."""
    template_name = 'SectionE/index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return the index page for QAR5 Section E."""
        assert isinstance(request, HttpRequest)
        qapp_id = request.GET.get('qapp_id', None)
        qapp = Qapp.objects.get(id=qapp_id)
        existing_references = References.objects.filter(qapp=qapp).first()

        # Update if existing, otherwise insert new:
        if existing_references:
            form = ReferencesForm(instance=existing_references)
        else:
            form = ReferencesForm({'qapp': qapp})

        return render(request, self.template_name,
                      {'title': 'QAR5 Section E', 'qapp_id': qapp_id,
                       'SECTION_E_INFO': SECTION_E_INFO, 'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a SectionE form filled out."""
        ctx = {'qapp_id': request.GET.get('qapp_id', None),
               'SECTION_E_INFO': SECTION_E_INFO, 'title': 'QAR5 Section E'}

        qapp = Qapp.objects.get(id=ctx['qapp_id'])
        existing_references = References.objects.filter(qapp=qapp).first()

        # Update if existing, otherwise insert new:
        if existing_references:
            ctx['form'] = ReferencesForm(instance=existing_references,
                                         data=request.POST)
        else:
            ctx['form'] = ReferencesForm(request.POST)

        if ctx['form'].is_valid():
            ctx['obj'] = ctx['form'].save(commit=True)
            ctx['save_success'] = 'Successfully Saved Changes!'

        return render(request, self.template_name, ctx)


class SectionFView(LoginRequiredMixin, TemplateView):
    """Class for processing QAPP Section F information, REVISIONS."""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return the index page for QAR5 Section F."""
        assert isinstance(request, HttpRequest)
        qapp_id = request.GET.get('qapp_id', None)
        revisions = Revision.objects.filter(qapp_id=qapp_id)
        return render(request, 'SectionF/index.html',
                      {'title': 'QAR5 Section F', 'qapp_id': qapp_id,
                       'SECTION_F_INFO': SECTION_F_INFO,
                       'revisions': revisions})


class RevisionCreate(LoginRequiredMixin, CreateView):
    """Class for creating new Revisions of a given QAPP."""

    template_name = 'SectionF/revision_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new QAPP."""
        qapp_id = request.GET.get('qapp_id', 0)
        qapp = Qapp.objects.get(id=qapp_id)
        form = RevisionForm({'qapp': qapp})
        ctx = {'form': form, 'qapp_id': qapp_id}

        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Project Lead form filled out."""
        form = RevisionForm(request.POST)
        qapp_id = form.data.get('qapp', '')
        #datetime_str = form.data['effective_date']
        #datetime_obj = datetime.strptime(datetime_str, DATETIME_FORMAT)
        #form.data['effective_date'] = datetime_obj
        if form.is_valid():
            obj = form.save(commit=True)
            return HttpResponseRedirect('/qar5/SectionF?qapp_id=%s' % qapp_id)

        ctx = {'form': form, 'qapp_id': qapp_id}
        return render(request, self.template_name, ctx)
