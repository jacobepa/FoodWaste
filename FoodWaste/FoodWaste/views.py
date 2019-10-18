"""
Definition of views.
"""

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView
from FoodWaste.forms import TrackingToolForm
from FoodWaste.models import TrackingTool


class TrackingToolList(ListView):
    """View for Secondary / Existing Data Tracking Tool"""
    model = TrackingTool
    context_object_name = 'tracking_tool_list'
    queryset = TrackingTool.objects.all()
    template_name = 'trackingtool/tracking_tool_list.html'


class TrackingToolCreate(CreateView):
    """Class for creating new Secondary / Existing Data"""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new Secondary / Existing Data"""
        return render(request, "trackingtool/tracking_tool_create.html",
                      {'form': TrackingToolForm()})


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'main/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'main/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
