from django import forms
from django.forms import widgets, ModelForm, ValidationError
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectDateWidget


from constants.models import *

from offices.models import *
from labs.models import *
from immediate_offices.models import *
from divisions.models import *
from branches.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36



		
class BranchForm(forms.ModelForm):
	"""
	A Form For Creating a Branch
	"""

	def __init__(self, *args, **kwargs):
		super(BranchForm, self).__init__(*args, **kwargs)
	
	division = forms.ModelChoiceField(label=_("Division this Branch is Under"), queryset=Division.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), required=True)	
	the_name = forms.CharField(label=_("Branch Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)	
	abbreviation = forms.CharField(label=_("Abbreviation"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	
	weblink = forms.CharField(label=_("Website Reference"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	ordering = forms.CharField(label=_("Ordering For Table Views"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	the_description = forms.CharField(label=_("Description of Project"), widget=forms.Textarea(attrs={'class':'form-control'}), required=False)
	
	attachment = forms.FileField(label="Upload A File If You Want To", required=False)
	
	class Meta:
		model = Branch
		fields = ("division", "the_name","abbreviation", "weblink", "ordering", "the_description", "attachment",)



	