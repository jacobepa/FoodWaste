# views.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301,E1101,R0901,W0613,W0622,C0411


"""Definition of views."""
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DeleteView
from os import path
from flowsa.forms import UploadForm
from flowsa.models import Upload


class FlowsaIndex(LoginRequiredMixin, TemplateView):
    """
    Class to return the main FLOWSA page along with a list of all
    FLOWSA uploaded files available to this user as well as a form for
    uploading new FLOWSA files. This class also handles the POSTs
    for new file uploads.
    """

    template_name = 'flowsa.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Return a view with an empty form for uploading new FLOWSA files
        in addition to a list of FLOWSA files available to the current user.
        """
        files_list = Upload.objects.filter(uploaded_by=request.user)
        return render(request, self.template_name,
                      {'form': UploadForm(), 'files': files_list})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new FLOWSA file upload."""
        form = UploadForm(request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.name = file.file.name
            file.save()
            data = {'is_valid': True, 'name': file.name,
                    'download_url': '/flowsa/download_file/%s' % file.id,
                    'delete_url': '/flowsa/delete_file/%s' % file.id}
        else:
            data = {'is_valid': False}

        return JsonResponse(data)


class FlowsaDelete(LoginRequiredMixin, DeleteView):
    """Class for deleting previously uploaded files."""
    
    model = Upload
    template_name = 'flowsa_upload_confirm_delete.html'
    success_url = reverse_lazy('flowsa:flowsa_index')


def flowsa_download(request):
    """Method for downloading a previously uploaded file."""
