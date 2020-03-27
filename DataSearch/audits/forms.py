from django import forms
from django.forms import widgets, ModelForm, ValidationError
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectDateWidget


from constants.models import *

from offices.models import *
from audits.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36



class AuditTypeForm(forms.ModelForm):
	"""
	A Form For Creating an AuditType
	"""

	def __init__(self, *args, **kwargs):
		super(AuditTypeForm, self).__init__(*args, **kwargs)
	
	the_name = forms.CharField(label=_("Audit Type"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	
	class Meta:
		model = AuditType
		fields = ("the_name", )
		

	