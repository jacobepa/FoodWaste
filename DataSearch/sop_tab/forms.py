from django import forms
from django.forms import widgets, ModelForm, ValidationError
from django.forms.models import inlineformset_factory, model_to_dict
from django.forms.widgets import SelectDateWidget

from constants.models import *
from constants.utils import *

from sop_tab.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from projects.models import *
from organization.models import *
from accounts.models import *
from constants.utils import setQuerySets
from django.db.models import Q

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name + " (" + obj.email + ")"

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name + " (" + obj.email + ")"
    # def label_from_instance(self, obj):
    #     return obj.display_value

class ProjectModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Add project title to label in dropdown if there is one.
        if obj.title and obj.qa_id: # Added safety check for qa_id value so + doesn't error
            label_idtitle = obj.qa_id + " " + obj.title
        else:
            label_idtitle = obj.qa_id
        return label_idtitle

class SOPModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Add sop title to label in dropdown if there is one.
        if obj.full_title and obj.sop_number: # Added safety check for sop_number value so + doesn't error
            label_idtitle = obj.sop_number + " " + obj.full_title
        else:
            label_idtitle = obj.sop_number
        return label_idtitle


# # # # # # #
#
# SOP TAB FORM ASYNC
# Copy of above but cleaned up and with 'async' fields instead of 'chosen-select' fields
#
# # # # # # #

class SOPTabFormAsync(forms.ModelForm):

    required_css_class = 'required'

    sop_status = forms.ModelChoiceField(label=_("Status"),
                                               queryset=SOPTab_Status.objects.filter(is_active="Y"),
                                               widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    full_title = forms.CharField(label=_("Full Title"), widget=forms.TextInput(attrs={"class": "form-control"}), required=True)

    keywords = forms.CharField(label=_("Keywords"), widget=forms.Textarea(attrs={'class': 'form-control'}),
                               required=False)

    comments = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={'class': 'form-control'}),
                               required=False)

    alt_id = forms.CharField(label=_("Alternate ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                                 required=False,
                                         help_text="The alternate ID can be used for a contractor's SOP ID in the case of extramural SOPs.")

    previous_id = forms.CharField(label=_("Previous ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                                  required=False,
                                         help_text="The previous ID can be used for any ID the SOP was assigned by EPA prior to being entered in or imported to QA Track.")

    sop_version = forms.IntegerField(label=_("Version"),
                                         widget=forms.TextInput(attrs={"class": "form-control"}), required=False,
                                         help_text="Leave blank unless an initial version number other than 0 is desired")

    office = forms.ModelChoiceField(label=_("Office"),
                                    queryset=Office.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    lab = forms.ModelChoiceField(label=_("Center"),
                                 queryset=Lab.objects.all(),
                                 widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    division = forms.ModelChoiceField(label=_("Division"),
                                  queryset=Division.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    branch = forms.ModelChoiceField(label=_("Branch"),
                                      queryset=Branch.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    discipline = forms.ModelChoiceField(label=_("Discipline"),
                                     queryset=Discipline.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    subdiscipline = forms.ModelChoiceField(label=_("Subdiscipline"),
                                  queryset=SubDiscipline.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    sop_contact = UserModelChoiceField(label=_("SOP Contact"),
                                       queryset=User.objects.none(),
                                       widget=forms.Select(attrs={"class": "form-control jasc-user-select",
                                                                  "data-placeholder": "Search people..."}),
                                       required=True)

    # Default to Intramural  (id = 2)
    mural_type = forms.ModelChoiceField(label=_("Intramural or Extramural"),
                                        queryset=SOPTab_MuralType.objects.filter(is_active="Y"),
                                        widget=forms.Select(attrs={'class': 'form-control'}), required=True, initial=2)

    # Default to Technical (id = 2)
    sop_type = forms.ModelChoiceField(label=_("SOP Type"),
                          queryset=SOPTab_Type.objects.filter(is_active="Y"),
                          widget=forms.Select(attrs={'class': 'form-control'}), required=True, initial=2)


    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    approving_manager = UserModelChoiceField(label=_("Approving QA Manager"),
                                          queryset=User.objects.none(),
                                          widget=forms.Select(attrs={"class": "form-control jasc-user-select",
                                                                     "data-placeholder": "Search people..."}),
                                          required=True)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    approving_line_manager = UserModelChoiceField(label=_("Approving Line Manager"),
                                             queryset=User.objects.none(),
                                             widget=forms.Select(attrs={"class": "form-control jasc-user-select", "data-placeholder": "Search people..."}),
                                             required=False,
                                             help_text="Required for intramural SOPs")

    date_approved = forms.DateField(label=_("Date Approved"),
                                    widget=forms.TextInput(attrs={'class': 'form-control date-control'}),
                                    required=False)

    date_reviewed = forms.DateField(label=_("Date of Last Review"),
                                    widget=forms.TextInput(attrs={'class': 'form-control date-control'}),
                                    required=False)

    date_effective = forms.DateField(label=_("Date Effective"),
                                    widget=forms.TextInput(attrs={'class': 'form-control date-control'}),
                                    required=False)

    #
    # API: Project.objects.all().order_by('qa_id')
    #
    projects = ProjectModelMultipleChoiceField(label=_("Projects"), widget=forms.SelectMultiple(
        attrs={'class': 'form-control jasc-project-select',
               'data-placeholder': 'Search projects . . .'}),
                                               queryset=Project.objects.none(),
                                               required=False)

    #
    # API: Program.objects.filter(is_active="Y")
    #
    programs = forms.ModelMultipleChoiceField(label=_("Programs"),
                                              queryset=Program.objects.none(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control jasc-program-select',
                                                                          'data-placeholder': 'Search programs . . .'}),
                                              required=False)

    #
    # API: SOPTab.objects.all().order_by('sop_number')
    #
    related_sops = SOPModelMultipleChoiceField(label=_("Related SOPs"), widget=forms.SelectMultiple(
        attrs={'class': 'form-control jasc-sop-select',
               'data-placeholder': 'Search SOPs . . .'}),
                                               queryset=SOPTab.objects.none(),
                                               required=False)

    #
    # API: ParticipatingOrganization.objects.none().order_by('company')
    #
    participating_orgs = forms.ModelMultipleChoiceField(label=_("EPA Non-ORD Organizations"), widget=forms.SelectMultiple(
        attrs={'class': 'form-control jasc-org-select',
               'data-placeholder': 'Search non-ORD orgs . . .'}),
                                               queryset=ParticipatingOrganization.objects.none(),
                                               required=False)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    sop_review_distribution_list = UserModelMultipleChoiceField(label=_("SOP Correspondence Email List (ORD)"),
                           widget=forms.SelectMultiple(attrs={'class': 'form-control jasc-user-select', 'data-placeholder': 'Search people . . .'}),
                           queryset=User.objects.none(),
                           required=False,
                           help_text='')

    sop_review_email_list = forms.CharField(label=_("Email List (non-ORD, separated by whitespace)"),
                                       widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                                       help_text='')

    def __init__(self, *args, **kwargs):
        super(SOPTabFormAsync, self).__init__(*args, **kwargs)

        async_filters = {
                "approving_manager" : (User,Q(userprofile__display_in_dropdowns="Y")),
                "sop_contact" : (User,Q(userprofile__display_in_dropdowns="Y")),
                "approving_line_manager" : (User,Q(userprofile__display_in_dropdowns="Y")),
                "projects" : (Project,True),
                "programs" : (Program,Q(is_active="Y")),
                "related_sops" : (SOPTab,True),
                "participating_orgs" : (ParticipatingOrganization,True),
                "sop_review_distribution_list" : (User,Q(userprofile__display_in_dropdowns="Y"))
            }

        setQuerySets(self,async_filters,kwargs)

    def clean(self):
        form_data = self.cleaned_data
        email_list = split_email_list(form_data['sop_review_email_list'])
        bad_emails = []
        for email in email_list:
            if not is_epa_email(email):
                bad_emails.append(email)
        if len(bad_emails):
            raise ValidationError({'sop_review_email_list':[non_epa_email_message(bad_emails),]})
        return form_data

    class Meta:
        model = SOPTab
        fields = (
                  "sop_status",
                  "full_title",
                  "keywords",
                  "comments",
                  "lab",
                  "office",
                  "lab",
                  "division",
                  "branch",
                  "discipline",
                  "subdiscipline",
                  "sop_type",
                  "mural_type",
                  "alt_id",
                  "previous_id",
                  "sop_version",
                  "sop_contact",
                  "approving_manager",
                  "approving_line_manager",
                  "date_approved",
                  "date_effective",
                  "date_reviewed",
                  "projects",
                  "programs",
                  "related_sops",
                  "participating_orgs",
                  "sop_review_distribution_list",
                  "sop_review_email_list",
        )
