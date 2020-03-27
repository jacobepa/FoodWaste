from django import forms
from django.forms import widgets, ModelForm, ValidationError
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectDateWidget


from constants.models import *

from offices.models import *
from persons.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36



		
class PersonForm(forms.ModelForm):
	"""
	A Form For Creating a Person
	"""

	def __init__(self, *args, **kwargs):
		super(PersonForm, self).__init__(*args, **kwargs)
	
	is_reviewer = forms.ChoiceField(label=_("Is Reviewer?"), choices=YN_CHOICES, widget=forms.Select(attrs={'class':'form-control'}), required=False)
	lab = forms.ModelChoiceField(label=_("Lab"), queryset=Lab.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), required=False)		
	first_name = forms.CharField(label=_("First Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)	
	last_name = forms.CharField(label=_("Last Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	
	class Meta:
		model = Person
		fields = ("is_reviewer", "lab", "first_name", "last_name",)
		
class PersonAdminForm(forms.ModelForm):
	"""
	A Form For Creating a Person
	"""

	def __init__(self, *args, **kwargs):
		super(PersonAdminForm, self).__init__(*args, **kwargs)
	
	person_status = forms.ModelChoiceField(label=_("Status"), queryset=PersonStatus.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), required=True)
	lab = forms.ModelChoiceField(label=_("Lab"), queryset=Lab.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), required=False)		
	first_name = forms.CharField(label=_("First Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)	
	last_name = forms.CharField(label=_("Last Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	badge_number = forms.CharField(label=_("Badge Number"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	is_reviewer = forms.ChoiceField(label=_("Can Review QA Activities"), choices=YN_CHOICES, widget=forms.Select(attrs={'class':'form-control'}), required=False)
	
	weblink = forms.CharField(label=_("Website Reference"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	the_description = forms.CharField(label=_("Description of Project Lead"), widget=forms.Textarea(attrs={'class':'form-control'}), required=False)
	
	attachment = forms.FileField(label="Upload A File If You Want To", required=False)
	
	class Meta:
		model = Person
		fields = ("person_status","lab", "first_name", "last_name", "badge_number", "is_reviewer", "weblink", "the_description", "attachment",)
		
class PersonTieForm(forms.ModelForm):
	"""
	A Form For Creating a Person
	"""

	def __init__(self, *args, **kwargs):
		super(PersonTieForm, self).__init__(*args, **kwargs)
	
	user = forms.ModelChoiceField(label=_("Tie Login User To Person"), queryset=User.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), required=True)	
	person_status = forms.ModelChoiceField(label=_("Status"), queryset=PersonStatus.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), required=True)	
	
	class Meta:
		model = Person
		fields = ("user", "person_status")
		
class PersonStatusForm(forms.ModelForm):
	"""
	A Form For Creating a Person
	"""

	def __init__(self, *args, **kwargs):
		super(PersonStatusForm, self).__init__(*args, **kwargs)
	
	the_name = forms.CharField(label=_("Person Status Type"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)		
	
	class Meta:
		model = PersonStatus
		fields = ("the_name", )




	