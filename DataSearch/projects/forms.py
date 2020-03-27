from django import forms
from django.forms import widgets, ModelForm, ValidationError
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectDateWidget

from accounts.models import *
from constants.models import *
from constants.utils import *

from projects.models import *
from organization.models import *
import organization.query_utils as oq

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.db.models import Q
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.core import serializers

from accounts.models import *

class ProjectStatusForm(forms.ModelForm):
    """
    A Form For Creating an Project Status
    """
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ProjectStatusForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("Project Status"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = ProjectStatus
        fields = ("the_name", "is_active")

class ProjectTypeForm(forms.ModelForm):
    """
    A Form For Creating an Project Type
    """
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ProjectTypeForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("Project Type"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = ProjectType
        fields = ("the_name", "is_active")

class QappStatusForm(forms.ModelForm):
    """
    A Form For Creating an QappStatus
    """
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(QappStatusForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("QAPP Status Type"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = QappStatus
        fields = ("the_name", "is_active")

class QaCategoryForm(forms.ModelForm):
    """
    A Form For Creating an QaCategory
    """

    def __init__(self, *args, **kwargs):
        super(QaCategoryForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("QA Category"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = QaCategory
        fields = ("the_name", "is_active")

class ProgramForm(forms.ModelForm):
    """
    A Form For Creating an Program
    """

    def __init__(self, *args, **kwargs):
        self.read_only = kwargs.pop('read_only') if 'read_only' in kwargs else False
        super(ProgramForm, self).__init__(*args, **kwargs)
        if self.read_only:
            self.fields['the_name'].widget.attrs['disabled'] = True
            self.fields['the_name'].required = False
            self.fields['is_active'].widget.attrs['disabled'] = True
            self.fields['is_active'].required = False

    required_css_class = 'required'

    the_name = forms.CharField(label=_("Program"), widget=forms.TextInput(attrs={'class':'form-control search'}), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(attrs={'class':'form-control'}), required=True)

    class Meta:
        model = Program
        fields = ("the_name", "is_active")

class NRMRLQAPPRequirementForm(forms.ModelForm):
    """
    A Form For Creating an NRMRLQAPPRequirement
    """

    def __init__(self, *args, **kwargs):
        super(NRMRLQAPPRequirementForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("NRMRL QAPP Requirement"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = NRMRLQAPPRequirement
        fields = ("the_name", "is_active")

class VehicleTypeForm(forms.ModelForm):
    """
    A Form For Creating an VehicleType
    """
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(VehicleTypeForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("Vehicle Type"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = VehicleType
        fields = ("the_name", "is_active")

class ExtramuralVehicleForm(forms.ModelForm):
    """
    A Form For Creating an Extramural Vehicle
    """

    def __init__(self, *args, **kwargs):
        self.read_only = kwargs.pop('read_only') if 'read_only' in kwargs else False
        super(ExtramuralVehicleForm, self).__init__(*args, **kwargs)
        self.fields['vehicle_type'].queryset = VehicleType.objects.filter(is_active="Y")
        if self.read_only:
            self.fields['the_name'].widget.attrs['disabled'] = True
            self.fields['the_name'].required = False
            self.fields['institution_name'].widget.attrs['disabled'] = True
            self.fields['institution_name'].required = False
            self.fields['vehicle_type'].widget.attrs['disabled'] = True
            self.fields['vehicle_type'].required = False
            self.fields['vehicle_number'].widget.attrs['disabled'] = True
            self.fields['vehicle_number'].required = False
            self.fields['is_active'].widget.attrs['disabled'] = True
            self.fields['is_active'].required = False

    required_css_class = 'required'

    the_name = forms.CharField(label=_("Extramural Vehicle"), widget=forms.TextInput(attrs={'class':'form-control search'}), required=True)


    institution_name = forms.CharField(label=_("Name of Contractor/Institution"),
                                       widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                       help_text="Use this field to identify the contractor or assistance agreement holder by name.")

    vehicle_type = forms.ModelChoiceField(label=_("Vehicle Type"),
                                          queryset=VehicleType.objects.none(),
                                          widget=forms.Select(attrs={'class': 'form-control form-control-subfield'}),
                                          required=True)

    vehicle_number = forms.CharField(label=_("Vehicle Number"), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     required=False,
                                     help_text="The official contract number, for example EP-C-08-015, found on the ORD QA Review Form.  Can also be used for the official assistance agreement number.")

    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(attrs={'class':'form-control'}), required=True)

    class Meta:
        model = ExtramuralVehicle
        fields = ("the_name", "institution_name", "vehicle_type", "vehicle_number", "is_active")

class ProjectCategoryForm(forms.ModelForm):
    """
    A Form For Creating an ProjectCategory
    """
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ProjectCategoryForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("Project Category"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = ProjectCategory
        fields = ("the_name", "is_active")

class ProjectLogTypeForm(forms.ModelForm):
    """
    A Form For Creating an ProjectCategory
    """
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ProjectLogTypeForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("QA Activity Type"), widget=forms.TextInput(), required=True)
    abbreviation = forms.CharField(label=_("Abbreviation"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = ProjectLogType
        fields = ("the_name", "abbreviation", "is_active")

class ReviewTypeForm(forms.ModelForm):
    """
    A Form For Creating an ReviewType
    """
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ReviewTypeForm, self).__init__(*args, **kwargs)

    the_name = forms.CharField(label=_("QA Review Type"), widget=forms.TextInput(), required=True)
    is_active = forms.ChoiceField(label=_("Is Active"), choices=YN_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = ReviewType
        fields = ("the_name", "is_active")

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name + " (" + obj.email + ")"

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name + " (" + obj.email + ")"


class RapProjectModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.IRMS_project_id

class RapTaskModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.RMSproject_id

class QAPPModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.qa_log_number + ": " + obj.title

# # # # # # #
#
# PROJECT FORM ASYNC - create/edit project
#
# # # # # # #
class ProjectFormAsync(forms.ModelForm):

    required_css_class = 'required'

    qa_id = forms.CharField(label=_("Project QA ID"),
                            widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                            required=True)

    previous_id = forms.CharField(label=_("Previous ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                                  required=False,
                                  help_text="The previous ID can be used for any ID the Project was assigned by EPA prior to being entered in or imported to QA Track.")

    alt_id = forms.CharField(label=_("Alternate ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                             required=False,
                             help_text="The alternate ID can be used for a number from another system.")

    title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={'class': 'form-control'}),
                            required=True)
    the_description = forms.CharField(label=_("Comments"),
                                      widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                                      required=False)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    person = UserModelChoiceField(label=_("Project Lead"),
                queryset=User.objects.none(),
                empty_label="",
                widget=forms.Select(attrs={'class': 'form-control jasc-user-select', 'data-placeholder': 'Search people . . .'}), required=True)

    created = forms.DateTimeField(label=_("Created"), widget=forms.DateInput(format='%Y-%m-%d %I:%M:%S %Z',
                                   attrs={'class':'form-control date-control','readonly': 'readonly'}), required=False)
    created_by = forms.CharField(label=_("Created By"), required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    modified = forms.DateTimeField(label=_("Last Modified"), widget=forms.DateInput(format='%Y-%m-%d %I:%M:%S %Z',
                                   attrs={'class':'form-control date-control','readonly': 'readonly'}), required=False)
    last_modified_by = forms.CharField(label=_("Last modified By"), required=False,
                                       widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))

    # these are only here for validation - use the organization_select.html widget
    office = forms.ModelChoiceField(label=_("Office"), queryset=Office.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    lab = forms.ModelChoiceField(label=_("Center"), queryset=Lab.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    division = forms.ModelChoiceField(label=_("Division"), queryset=Division.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    branch = forms.ModelChoiceField(label=_("Branch"), queryset=Branch.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    collaborators = UserModelMultipleChoiceField(label=_("Team Member(s)"),
                        widget=forms.SelectMultiple(attrs={'class': 'form-control jasc-user-select', 'data-placeholder': 'Search people . . .'}),
                        queryset = User.objects.none(), required=False)


    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    qa_manager = UserModelChoiceField(label=_("QA Manager"),
                                  queryset=User.objects.none(),
                                  empty_label="",
                                  widget=forms.Select(attrs={'class': 'form-control jasc-user-select',
                                                             'data-placeholder': 'Search people . . .'}), required=True)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    previous_qams = UserModelMultipleChoiceField(label=_("Previous QA Manager(s)"),
                                                 widget=forms.SelectMultiple(
                                                     attrs={'class': 'form-control jasc-user-select',
                                                            'data-placeholder': 'Search people . . .'}),
                                                 queryset=User.objects.none(), required=False)


    #
    # API: ParticipatingOrganization.objects.none().order_by('company')
    #
    participating_organizations = \
        forms.ModelMultipleChoiceField(label=_("EPA Non-ORD Organization(s)"),
                                       widget=forms.SelectMultiple(attrs={'class': 'form-control jasc-org-select',
                                                                          'data-placeholder': 'Search non-ORD orgs . . .'}),
                                       queryset = ParticipatingOrganization.objects.none(), required=False, help_text="Typically used to identify non-ORD EPA organizations participating in the research AND for which no contract or assistance agreement exists.  Note: Use the field “Name of Contractor/Institution” to identify contractors and assistance agreement holders.")

    ace_rap_numbers = forms.CharField(label=_("ACE RAP Numbers"), widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}), required=False)
    css_rap_numbers = forms.CharField(label=_("CSS RAP Numbers"), widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}), required=False)
    sswr_rap_numbers = forms.CharField(label=_("SSWR RAP Numbers"), widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}), required=False)
    hhra_rap_numbers = forms.CharField(label=_("HHRA RAP Numbers"), widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}), required=False)
    hsrp_rap_numbers = forms.CharField(label=_("HSRP RAP Numbers"), widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}), required=False)
    hsrp_rap_extensions = forms.CharField(label=_("HSRP Extensions"), widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}), required=False)
    shc_rap_numbers = forms.CharField(label=_("SHC RAP Numbers"), widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}), required=False)

    #
    # API: Program.objects.filter(is_active="Y")
    #
    programs = forms.ModelMultipleChoiceField(label=_("Program(s)"),
                            widget = forms.SelectMultiple(attrs={'class': 'form-control jasc-program-select', 'data-placeholder': 'Search programs . . .'}),
                                              queryset=Program.objects.none(), required=False)

    project_status = forms.ModelChoiceField(label=_("Project Status"),
                                        #queryset=ProjectStatus.objects.none(),
                                        queryset=ProjectStatus.objects.filter(is_active="Y").order_by('sort_number'),
                                        widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    qa_category = forms.ModelChoiceField(label=_("QA Category"), queryset=QaCategory.objects.none(),
                                         widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    nrmrl_qapp_requirement = forms.ModelMultipleChoiceField(label=_("Project Type"),
                                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                                            queryset=NRMRLQAPPRequirement.objects.none(),
                                                            required=False)
    project_type = forms.ModelChoiceField(label=_("Intramural or Extramural"),
                                          queryset=ProjectType.objects.none(),
                                          widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    # extramural_vehicle = forms.ModelChoiceField(label=_("Extramural Vehicle"),
    #                                       queryset=ExtramuralVehicle.objects.none(),
    #                                       widget=forms.Select(attrs={'class': 'form-control form-control-subfield'}),
    #                                       required=False)

    vehicle_type = forms.ModelChoiceField(label=_("Vehicle Type"),
                                          queryset=VehicleType.objects.none(),
                                          widget=forms.Select(attrs={'class':'form-control form-control-subfield'}), required=False)

    institution_name = forms.CharField(label=_("Name of Contractor/Institution"), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, help_text="Use this field to identify the contractor or assistance agreement holder by name.  Note:  Use the field “EPA Non-ORD Organization” to identify an organization for which no contract or assistance agreement exists.")

    vehicle_number = forms.CharField(label=_("Vehicle Number"), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, help_text="The official contract number, for example EP-C-08-015, found on the ORD QA Review Form.  Can also be used for the official assistance agreement number.")
    date_project_identified = forms.CharField(label=_("Date Project Identified"),
                                              widget=forms.TextInput(attrs={'class': 'form-control date-control'}), required=True)

    qapp_status = forms.ModelChoiceField(label=_("QAPP Status"), queryset=QappStatus.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    restrict_qapp_files = forms.TypedChoiceField(label=_("Restrict access to QAPP QA activity attachments"), choices=BOOLEAN_YES_NO,
                                     widget=forms.Select(attrs={'class': 'form-control'}), required=True, help_text="If yes, access to any files attached to QAPP QA activities for this project will be restricted to project editors and users associated with the project. In addition, any files marked as the latest approved QAPP for this project will NOT be posted on ORD@Work. See user manual for more details.")
    restrict_ext_package_files = forms.TypedChoiceField(label=_("Restrict access to EP QA activity attachments"), choices=BOOLEAN_YES_NO,
                                     widget=forms.Select(attrs={'class': 'form-control'}), required=True, help_text="If yes, access to any files attached to the latest Extramural Package QA activity for this project will be restricted to project editors and users associated with the project. See user manual for more details.")
    qapp_approval_date = forms.CharField(label=_("QAPP Approval Date"),
                                         widget=forms.TextInput(attrs={'class': 'form-control date-control'}), required=False)

    last_qapp_review_date = forms.CharField(label=_("Latest Annual QAPP Review Date"),
                                         widget=forms.TextInput(attrs={'class': 'form-control date-control'}),
                                         required=False, help_text="This date will automatically update if a new QA activity is created.  If no new QA activity is created, this date should be updated manually by editing the date.  For example, if the Project Lead reviews the QAPP and no changes are needed, the QA Manager should enter the date of review by the Project Lead.")

    qmp_required = forms.ChoiceField(label=_("QMP Required"), choices=YN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    qmp_approval_date = forms.CharField(label=_("QMP Approval Date"),
                                        widget=forms.TextInput(attrs={'class': 'form-control date-control'}), required=False)

    weblink = forms.CharField(label=_("Links"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False, help_text="URLs to related projects in QA Track and/or any associated project websites can be entered here. Separate multiple links with a space.")

    def __init__(self, is_editable, is_new, office_id, lab_id, division_id, branch_id, *args, **kwargs):
        self.is_new = is_new
        # self.is_editable = is_editable
        super(ProjectFormAsync, self).__init__(*args, **kwargs)

        self.fields['qa_category'].queryset = QaCategory.objects.filter(is_active="Y")
        #self.fields['programs'].queryset = Program.objects.filter(is_active="Y")
        self.fields['nrmrl_qapp_requirement'].queryset = NRMRLQAPPRequirement.objects.filter(is_active="Y")
        self.fields['project_type'].queryset = ProjectType.objects.filter(is_active="Y")
        self.fields['project_status'].queryset = ProjectStatus.objects.filter(is_active="Y")
        #self.fields['extramural_vehicle'].queryset = ExtramuralVehicle.objects.filter(is_active="Y")
        self.fields['vehicle_type'].queryset = VehicleType.objects.filter(is_active="Y")
        self.fields['qapp_status'].queryset = QappStatus.objects.filter(is_active="Y")

        # Set the initial value of QA Manager to be the project org's QA manager. There can be more than one, so just take the first.
        self.fields['qa_manager'].queryset = User.objects.filter(Q(userprofile__display_in_dropdowns="Y")
                                                                 | Q(id__in=[168])
                                                                 ).order_by('last_name', 'first_name', 'email')
        org_qams = get_qamanagers(office_id, lab_id, division_id, branch_id)
        qa_manager = org_qams.first()
        self.fields['qa_manager'].initial = qa_manager.id

        if self.is_new:
            self.fields['qa_id'].required = False

        async_filters = {
            "person": (User, Q(userprofile__display_in_dropdowns="Y")),
            "collaborators": (User, Q(userprofile__display_in_dropdowns="Y")),
            "qa_manager": (User, Q(userprofile__display_in_dropdowns="Y")),
            "previous_qams": (User, Q(userprofile__display_in_dropdowns="Y")),
            "programs": (Program, Q(is_active="Y")),
            "participating_organizations": (ParticipatingOrganization, True)
        }

        setQuerySets(self, async_filters, kwargs)

    class Meta:
        model = Project
        fields = (
                "qa_id", "title", "the_description", "person", "created", "created_by", "modified", "last_modified_by",
                "office", "lab", "division", "branch", "collaborators", "qa_manager", "previous_qams",
                "programs", "project_status", "alt_id",
                "previous_id", "qa_category",
                "ace_rap_numbers", "css_rap_numbers", "sswr_rap_numbers",
                "hhra_rap_numbers", "hsrp_rap_numbers", "hsrp_rap_extensions", "shc_rap_numbers",
                "nrmrl_qapp_requirement", "project_type",
                #"extramural_vehicle",
                "vehicle_type", "institution_name", "vehicle_number",
                "date_project_identified", "qapp_status", "restrict_qapp_files","restrict_ext_package_files", "qapp_approval_date", "last_qapp_review_date", "qmp_required", "qmp_approval_date",
                "weblink", "participating_organizations"
        )

# Commented out to see if this is not needed. Did not find any references to it.
# class ProjectCollaboratorInlineFormset(forms.ModelForm):
#
#     required_css_class = 'required'
#
#     def __init__(self, *args, **kwargs):
#         super(ProjectCollaboratorInlineFormset, self).__init__(*args, **kwargs)
#
#     person = forms.ModelMultipleChoiceField(label=_("Team Member"), queryset=User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email'), required=False)
#
#     class Meta:
#         model = Person
#         fields = ("person",)


# # # # # # #
#
# QA ACTIVITY FORM ASYNC - clone/edit so know QA activity type
#
# # # # # # #
class ProjectLogFormAsync(forms.ModelForm):

    required_css_class = 'required'

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    technical_lead = UserModelChoiceField(label=_("QA Activity POC:"),
                                          queryset=User.objects.none(),
                                          empty_label="",
                                          widget=forms.Select(attrs={"class": "form-control jasc-user-select", "data-placeholder": "Search people..."}),
                                          required=True)

    previous_id = forms.CharField(label=_("Previous ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                                  required=False,
                                  help_text="The previous ID can be used for any ID the QA Activity was assigned by EPA prior to being entered in or imported to QA Track.")

    alt_id = forms.CharField(label=_("Alternate ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                             required=False,
                             help_text="The alternate ID can be used for a number from another system.")

    title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True)

    # these are only here for validation - use the organization_select.html widget
    office = forms.ModelChoiceField(label=_("Office"), queryset=Office.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    lab = forms.ModelChoiceField(label=_("Center"), queryset=Lab.objects.all(),
                                 widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    division = forms.ModelChoiceField(label=_("Division"), queryset=Division.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    branch = forms.ModelChoiceField(label=_("Branch"), queryset=Branch.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    qa_review_required = forms.ChoiceField(label=_("QA Review Required"), choices=YN_CHOICES, widget=forms.Select(attrs={"class": "form-control"}), required=False)

    qapp = QAPPModelChoiceField(label=_("QAPP QA Activity Number/Title"), queryset=ProjectLog.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control chosen-select'}),
                                required=False,
                                help_text="The purpose of this field is to reference the approved QAPP for the product being reviewed.  To reference an approved QAPP not in the dropdown (e.g., from a different project), use the Comments field when you create or edit the review.  Some product types might not require an entry, for example review of an extramural package prior to award, and the field can be left blank.")
    # qapp = forms.ModelChoiceField(label=_("QAPP QA Activity"), queryset=ProjectLog.objects.all(), widget=forms.Select(attrs={"class":"form-control chosen-select"}), required=False)
    # qapp = QAPPModelChoiceField(label=_("QAPP QA Activity"), queryset=ProjectLog.objects.none(), widget=forms.Select(attrs={"class": "form-control jasc-projectlog-select",
    #                                                            "data-placeholder": "Select relevant QAPP..."}), required=False, help_text="To reference a QAPP from a different project to include in the review form, enter it in the Comments field when you create or edit the review.")

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    reviewer = UserModelChoiceField(label=_("Reviewer"),
                                    queryset=User.objects.none(),
                                    widget=forms.Select(attrs={"class": "form-control jasc-user-select",
                                                               "data-placeholder": "Search people..."}), required=False, help_text="The reviewer is typically the QA manager.")
    the_name = forms.CharField(label=_("Keyword Search Field"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
    software_status = forms.ChoiceField(label=_("If Software, Active or Inactive"), choices=STATUS_CHOICES, widget=forms.Select(attrs={"class":"form-control"}), required=False)

    date_review_requested = forms.CharField(label=_("Date Review Requested"),
                                              widget=forms.TextInput(attrs={'class': 'form-control date-control', 'id':'datepicker4'}),
                                              required=False)
    date_received = forms.CharField(label=_("Date Received"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker1'}), required=False)
    date_reviewed = forms.CharField(label=_("Date Reviewed"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker2'}), required=False)
    date_approved = forms.CharField(label=_("Date Approved"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker3'}), required=False)

    review_type = forms.ModelChoiceField(label=_("Review Recommendation"), queryset=ReviewType.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), required=False)

    lco_tracking_number = forms.CharField(label=_("STICS Clearance Tracking Number"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
    product_category = forms.ModelChoiceField(label=_("Product Category"), queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), required=True)

    weblink = forms.CharField(label=_("Links"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False, help_text="URLs to related projects in QA Track and/or any associated project websites can be entered here. Separate multiple links with a space.")
    the_description = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={"class":"form-control"}), required=False)

    def __init__(self, *args, **kwargs):
        super(ProjectLogFormAsync, self).__init__(*args, **kwargs)

        async_filters = {
            "technical_lead": (User, Q(userprofile__display_in_dropdowns="Y")),
            "reviewer": (User, Q(userprofile__display_in_dropdowns="Y"))
        }

        setQuerySets(self, async_filters, kwargs)

        self.fields['qapp'].queryset = ProjectLog.objects.filter(Q(project=self.instance.project) & Q(project_log_type__the_name__iexact='QAPP'))


    class Meta:
        model = ProjectLog
        fields = ("technical_lead", "title", "alt_id",
                "previous_id", "reviewer", "qa_review_required", "qapp", "the_name", "software_status", "date_review_requested", "date_received", "date_reviewed", "date_approved",
        "review_type", "lco_tracking_number", "product_category", "weblink", "the_description", "office", "lab", "division", "branch")

# Commented out to test that it's not in use
# class ProjectLogNoLogTypeForm(forms.ModelForm):
#     """
#     A Form For Creating an Project
#     """
#     required_css_class = 'required'
#
#     def __init__(self, *args, **kwargs):
#         super(ProjectLogNoLogTypeForm, self).__init__(*args, **kwargs)
#         # self.fields['reviewer'].queryset = User.objects.filter(userprofile__is_reviewer="Y")
#
#         activpoc_id = self.instance.technical_lead_id
#         self.fields['technical_lead'].queryset = User.objects.filter(
#             Q(userprofile__display_in_dropdowns="Y") | Q(id=activpoc_id)).order_by('last_name', 'first_name', 'email')
#
#         rev_id = self.instance.reviewer_id
#         self.fields['reviewer'].queryset = User.objects.filter(
#             (Q(userprofile__display_in_dropdowns="Y") & Q(userprofile__is_reviewer="Y")) | Q(id=rev_id)).order_by(
#             'last_name', 'first_name', 'email')
#
#
#     technical_lead = forms.ModelChoiceField(label=_("QA Activity POC:"),
#                                             #queryset=User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email'),
#                                             queryset=User.objects.none(),
#                                             widget=forms.Select(attrs={"class":"form-control"}), required=True)
#
#     title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True)
#     qa_review_required = forms.ChoiceField(label=_("QA Review Required"), choices=YN_CHOICES, widget=forms.Select(attrs={"class":"form-control"}), required=False)
#     reviewer = forms.ModelChoiceField(label=_("Reviewer"),
#                                       #queryset=User.objects.filter(Q(userprofile__display_in_dropdowns="Y") & Q(userprofile__is_reviewer="Y")).order_by('last_name', 'first_name', 'email'),
#                                       queryset=User.objects.none(),
#                                       widget=forms.Select(attrs={"class":"form-control"}), required=False)
#     the_name = forms.CharField(label=_("Keyword Search Field"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
#     software_status = forms.ChoiceField(label=_("If Software, Active or Inactive"),choices=STATUS_CHOICES, widget=forms.Select(attrs={"class":"form-control"}), required=False)
#
#     qa_log_number_x = forms.IntegerField(label=_("QA Activity Number X"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True, help_text="Just X part of S-30000-QP-X-Y ie 1...Scroll To Bottom of Page To See If QA Activities Exist For This Project.")
#     qa_log_number_y = forms.IntegerField(label=_("QA Activity Number Y"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True, help_text="Just Y part of S-30000-QP-X-Y ie 4...If You Accidently Duplicate a Number QA Track Will Auto Increment To The Next Available Number")
#     date_received = forms.CharField(label=_("Date Received"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker1'}), required=False)
#     date_reviewed = forms.CharField(label=_("Date Reviewed"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker2'}), required=False)
#     date_approved = forms.CharField(label=_("Date Approved"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker3'}), required=False)
#
#     review_type = forms.ModelChoiceField(label=_("Review Recommendation"), queryset=ReviewType.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), required=False)
#
#     lco_tracking_number = forms.CharField(label=_("STICS Clearance Tracking Number"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
#
#
#     weblink = forms.CharField(label=_("Website Reference"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
#     the_description = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={"class":"form-control"}), required=False)
#
#     class Meta:
#         model = ProjectLog
#         fields = ("technical_lead", "title", "qa_review_required", "reviewer", "the_name", "software_status", "qa_log_number_x", "qa_log_number_y", "date_received", "date_reviewed", "date_approved",
#         "review_type", "lco_tracking_number", "weblink", "the_description",)

# # # # # # #
#
# AUDIT QA ACTIVITY FORM ASYNC - create/edit audit qa activity
#
# # # # # # #
class ProjectLogAuditFormAsync(forms.ModelForm):

    required_css_class = 'required'

    audit_type = forms.ModelChoiceField(label=_("Audit Type"), queryset=AuditType.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), required=False)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    technical_lead = UserModelChoiceField(label=_("Audit POC:"),
                                          queryset=User.objects.none(),
                                          empty_label="",
                                          widget=forms.Select(attrs={"class":"form-control jasc-user-select", "data-placeholder":"Search people..."}), required=True)

    title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True)

    qa_log_number_x = forms.IntegerField(label=_("QA Activity - Audit Number X"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True, help_text="Just X part of S-30000-QP-X-Y ie 1...Scroll To Bottom of Page To See If QA Activities Exist For This Project.")
    qa_log_number_y = forms.IntegerField(label=_("QA Activity - Audit Number Y"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True, help_text="Just Y part of S-30000-QP-X-Y ie 4...If You Accidently Duplicate a Number QA Track Will Auto Increment To The Next Available Number")

    previous_id = forms.CharField(label=_("Previous ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                                  required=False,
                                  help_text="The previous ID can be used for any ID the QA Activity was assigned by EPA prior to being entered in or imported to QA Track.")

    alt_id = forms.CharField(label=_("Alternate ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                             required=False,
                             help_text="The alternate ID can be used for a number from another system.")

    date_review_requested = forms.CharField(label=_("Date Review Requested"),
                                            widget=forms.TextInput(
                                                attrs={'class': 'form-control', 'id': 'datepicker4'}),
                                            required=False)
    date_received = forms.CharField(label=_("Date Received (Date of Audit or Date Response Received)"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker1'}), required=False)
    date_reviewed = forms.CharField(label=_("Date Reviewed (Date Final Audit Report Submitted or Date Responses Reviewed)"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker2'}), required=False)
    date_approved = forms.CharField(label=_("Date Approved (Date Audit Closed)"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker3'}), required=False)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    reviewer = UserModelChoiceField(label=_("Audit Reviewer"),
                                    queryset=User.objects.none(),
                                    widget=forms.Select(attrs={"class":"form-control jasc-user-select", "data-placeholder":"Search people..."}), required=False, empty_label="")

    qa_review_required = forms.ChoiceField(label=_("QA Review Required"), choices=YN_CHOICES, widget=forms.Select(attrs={"class": "form-control"}), required=False)

    auditor = forms.CharField(label=_("Auditor"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
    auditor_organization = forms.CharField(label=_("Auditor Organization"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)

    audit_location = forms.CharField(label=_("Audit Location"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
    organization = forms.CharField(label=_("Organization Being Audited"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
    audit_date = forms.CharField(label=_("Audit Date"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker6'}), required=False)

    review_type = forms.ModelChoiceField(label=_("Review Recommendation"), queryset=ReviewType.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), required=False)
    number_of_finding = forms.CharField(label=_("Number of Findings"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)

    the_description = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={"class":"form-control"}), required=False)

    def __init__(self, *args, **kwargs):
        super(ProjectLogAuditFormAsync, self).__init__(*args, **kwargs)

        async_filters = {
            "technical_lead": (User, Q(userprofile__display_in_dropdowns="Y")),
            "reviewer": (User, Q(userprofile__display_in_dropdowns="Y"))
        }

        setQuerySets(self, async_filters, kwargs)

        # activpoc_id = self.instance.technical_lead_id
        # self.fields['technical_lead'].queryset = User.objects.filter(
        #     Q(userprofile__display_in_dropdowns="Y") | Q(id=activpoc_id)).order_by('last_name', 'first_name', 'email')
        #
        # rev_id = self.instance.reviewer_id
        # self.fields['reviewer'].queryset = User.objects.filter(
        #     (Q(userprofile__display_in_dropdowns="Y") & Q(userprofile__is_reviewer="Y")) | Q(id=rev_id)).order_by(
        #     'last_name', 'first_name', 'email')

    class Meta:
        model = ProjectLog
        fields = ("audit_type", "technical_lead", "title", "qa_log_number_x", "qa_log_number_y", "alt_id", "previous_id", "date_received", "date_reviewed", "date_approved", "reviewer", "qa_review_required", "auditor", "auditor_organization", "audit_location",
        "organization", "audit_date", "review_type", "number_of_finding", "the_description","date_review_requested",)

# # # # # # #
#
# QA ACTIVITY FORM ASYNC - creating an activity, don't know activity type
#
# # # # # # #
class ProjectLogNoProjectFormAsync(forms.ModelForm):

    required_css_class = 'required'

    project_log_type = forms.ModelChoiceField(label=_("QA Activity Type"), queryset=ProjectLogType.objects.none(), widget=forms.Select(attrs={"class":"form-control"}), required=True)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    technical_lead = UserModelChoiceField(label=_("QA Activity POC:"),
                                          queryset=User.objects.none(),
                                          empty_label="",
                                          widget=forms.Select(attrs={"class":"form-control jasc-user-select", "data-placeholder":"Search people..."}), required=True)

    title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True)

    qa_log_number_x = forms.IntegerField(label=_("QA Activity Number X"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True, help_text="Just X part of N-DIV-0030000-QP-X-Y ie 1...Scroll To Bottom of Page To See If  Activities Exist For This Project.")
    qa_log_number_y = forms.IntegerField(label=_("QA Activity Number Y"), widget=forms.TextInput(attrs={"class":"form-control"}), required=True, help_text="Just Y part of N-DIV-0030000-QP-X-Y ie 4...If You Accidently Duplicate a Number QA Track Will Auto Increment To The Next Available Number")

    previous_id = forms.CharField(label=_("Previous ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                                  required=False,
                                  help_text="The previous ID can be used for any ID the QA Activity was assigned by EPA prior to being entered in or imported to QA Track.")

    alt_id = forms.CharField(label=_("Alternate ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                             required=False,
                             help_text="The alternate ID can be used for a number from another system.")

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    reviewer = UserModelChoiceField(label=_("Reviewer"),
                                    queryset=User.objects.none(),
                                    empty_label="",
                                    widget=forms.Select(attrs={"class":"form-control jasc-user-select", "data-placeholder":"Search people..."}), required=False,
                                    help_text="The reviewer is typically the QA manager.") # these are only here for validation - use the organization_select.html widget

    office = forms.ModelChoiceField(label=_("Office"), queryset=Office.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    lab = forms.ModelChoiceField(label=_("Center"), queryset=Lab.objects.all(),
                                 widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    division = forms.ModelChoiceField(label=_("Division"), queryset=Division.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    branch = forms.ModelChoiceField(label=_("Branch"), queryset=Branch.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    # the_name = forms.CharField(label=_("Keyword Search Field"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)
    qa_review_required = forms.ChoiceField(label=_("QA Review Required"), choices=YN_CHOICES, widget=forms.Select(attrs={"class":"form-control"}), required=False)

    qapp = QAPPModelChoiceField(label=_("QAPP QA Activity Number/Title"), queryset=ProjectLog.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control chosen-select'}),
                                required=False,
                                help_text="The purpose of this field is to reference the approved QAPP for the product being reviewed.  To reference an approved QAPP not in the dropdown (e.g., from a different project), use the Comments field when you create or edit the review.  Some product types might not require an entry, for example review of an extramural package prior to award, and the field can be left blank.")
    #qapp = forms.ModelChoiceField(label=_("QAPP QA Activity"), queryset=ProjectLog.objects.all(), widget=forms.Select(attrs={"class": "form-control chosen-select"}), required=False)

    date_review_requested = forms.CharField(label=_("Date Review Requested"),
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'id':'datepicker4'}),
                                       required=False)
    date_received = forms.CharField(label=_("Date Received"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker1'}), required=False)
    date_reviewed = forms.CharField(label=_("Date Reviewed"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker2'}), required=False)
    date_approved = forms.CharField(label=_("Date Approved"), widget=forms.TextInput(attrs={'class':'form-control', 'id':'datepicker3'}), required=False)

    review_type = forms.ModelChoiceField(label=_("Review Recommendation"), queryset=ReviewType.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), required=False)
    lco_tracking_number = forms.CharField(label=_("STICS Clearance Tracking Number"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False)

    product_category = forms.ModelChoiceField(label=_("Product Category"), queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=True)

    software_status = forms.ChoiceField(label=_("If Software, Active or Inactive"),choices=STATUS_CHOICES, widget=forms.Select(attrs={"class":"form-control"}), required=False)
    weblink = forms.CharField(label=_("Links"), widget=forms.TextInput(attrs={"class":"form-control"}), required=False, help_text="URLs to related projects in QA Track and/or any associated project websites can be entered here. Separate multiple links with a space.")
    the_description = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={"class":"form-control"}), required=False)

    def __init__(self, *args, **kwargs):
        super(ProjectLogNoProjectFormAsync, self).__init__(*args, **kwargs)

        self.fields['project_log_type'].queryset = ProjectLogType.objects.filter(is_active="Y")

        async_filters = {
            "technical_lead": (User, Q(userprofile__display_in_dropdowns="Y")),
            "reviewer": (User, Q(userprofile__display_in_dropdowns="Y"))
        }

        setQuerySets(self, async_filters, kwargs)

        self.fields['qapp'].queryset = ProjectLog.objects.filter(Q(project=self.initial['project']) & Q(project_log_type__the_name__iexact='QAPP'))

        # activpoc_id = self.instance.technical_lead_id
        # self.fields['technical_lead'].queryset = User.objects.filter(
        #     Q(userprofile__display_in_dropdowns="Y") | Q(id=activpoc_id)).order_by('last_name', 'first_name', 'email')
        #
        # rev_id = self.instance.reviewer_id
        # self.fields['reviewer'].queryset = User.objects.filter(
        #     (Q(userprofile__display_in_dropdowns="Y") & Q(userprofile__is_reviewer="Y")) | Q(id=rev_id)).order_by(
        #     'last_name', 'first_name', 'email')

    class Meta:
        model = ProjectLog
        fields = ("project_log_type", "technical_lead", "title", "qa_log_number_x", "qa_log_number_y", "alt_id", "previous_id", "reviewer",
                  "qa_review_required", "qapp", "date_review_requested", "date_received", "date_reviewed", "date_approved",
                  "review_type", "lco_tracking_number", "product_category", "software_status", "weblink", "the_description",
                  "office", "lab", "division", "branch")


# Commented out to check it's not in use
# class ProjectLogReviewForm(forms.ModelForm):
#     """
#     A Form For Creating an Project
#     """
#     required_css_class = 'required'
#
#     def __init__(self, *args, **kwargs):
#         super(ProjectLogReviewForm, self).__init__(*args, **kwargs)
#         # self.fields['reviewer'].queryset = User.objects.filter(userprofile__is_reviewer="Y")
#
#         rev_id = self.instance.reviewer_id
#         self.fields['reviewer'].queryset = User.objects.filter(
#             (Q(userprofile__display_in_dropdowns="Y") & Q(userprofile__is_reviewer="Y")) | Q(id=rev_id)).order_by(
#             'last_name', 'first_name', 'email')
#
#     reviewer = forms.ModelChoiceField(label=_("Reviewer"),
#                                       #queryset=User.objects.filter(Q(userprofile__display_in_dropdowns="Y") & Q(userprofile__is_reviewer="Y")).order_by('last_name', 'first_name', 'email'),
#                                       queryset=User.objects.none(),
#                                       widget=forms.Select(), required=False)
#     review_type = forms.ModelChoiceField(label=_("QA Review Result"), queryset=ReviewType.objects.all(), widget=forms.Select(), required=False)
#     the_description = forms.CharField(label=_("Review and Distribution History"), widget=forms.Textarea(), required=False)
#
#     class Meta:
#         model = ProjectLog
#         fields = ("reviewer", "review_type", "the_description",)

# # # # # # #
#
# QA ACTIVITY REVIEW FORM ASYNC - create/edit QA activity review
#
# # # # # # #
class QaReviewFormAsync(forms.ModelForm):

    required_css_class = 'required'

    qa_review_distribution_list = UserModelMultipleChoiceField(label=_("Email List (ORD)"),
                        widget=forms.SelectMultiple(attrs={'class': 'form-control jasc-user-select', 'data-placeholder': 'Search people . . .'}),
                        queryset=User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email'), required=False)

    qa_review_email_list = forms.CharField(label=_("Email List (non-ORD, separated by whitespace)"),
                                           widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    reviewer = UserModelChoiceField(label=_("Reviewer"),
                                    queryset=User.objects.none(),
                                    empty_label="",
                widget=forms.Select(attrs={'class': 'form-control jasc-user-select', 'data-placeholder': 'Search people . . .'}), required=True)

    date_reviewed = forms.CharField(label=_("Date Reviewed"),
                                    widget=forms.TextInput(attrs={'class':'form-control date-control'}), required=False)
    date_approved = forms.CharField(label=_("Date Approved"),
                                    widget=forms.TextInput(attrs={'class':'form-control date-control'}), required=False)

    review_type = forms.ModelChoiceField(label=_("Review Recommendation"),
                                         queryset=ReviewType.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    qa_review_comment = forms.CharField(label=_("Comments"),
                                        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)

    def __init__(self, *args, **kwargs):
        super(QaReviewFormAsync, self).__init__(*args, **kwargs)

        async_filters = {
            "qa_review_distribution_list": (User, Q(userprofile__display_in_dropdowns="Y")),
            "reviewer": (User, Q(userprofile__display_in_dropdowns="Y"))
        }

        setQuerySets(self, async_filters, kwargs)

        # rev_id = self.instance.reviewer_id
        # self.fields['reviewer'].queryset = User.objects.filter(
        #     (Q(userprofile__display_in_dropdowns="Y") & Q(userprofile__is_reviewer="Y")) | Q(id=rev_id)).order_by(
        #     'last_name', 'first_name', 'email')

    def clean(self):
        form_data = self.cleaned_data
        email_list = split_email_list(form_data['qa_review_email_list'])
        bad_emails = []
        for email in email_list:
            if not is_epa_email(email):
                bad_emails.append(email)
        if len(bad_emails):
            raise ValidationError({'qa_review_email_list':[non_epa_email_message(bad_emails),]})
        return form_data

    class Meta:
        model = ProjectLog
        fields = ("qa_review_email_list", "reviewer", "date_reviewed", "date_approved", "review_type", "qa_review_comment", "qa_review_distribution_list")

# # # # # # #
#
# PARTICIPATING ORGANIZATION FORM - EPA NON-ORD ORGANIZATION
#
# # # # # # #
class ParticipatingOrganizationForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.read_only = kwargs.pop('read_only') if 'read_only' in kwargs else False
        super(ParticipatingOrganizationForm, self).__init__(*args, **kwargs)
        if self.read_only:
            self.fields['company'].widget.attrs['disabled'] = True
            self.fields['company'].required = False
            self.fields['mail_to_name'].widget.attrs['disabled'] = True
            self.fields['mail_to_name'].required = False
            self.fields['mail_to_address'].widget.attrs['disabled'] = True
            self.fields['mail_to_address'].required = False
            self.fields['mail_to_city'].widget.attrs['disabled'] = True
            self.fields['mail_to_city'].required = False
            self.fields['mail_to_state'].widget.attrs['disabled'] = True
            self.fields['mail_to_state'].required = False
            self.fields['email_address_epa'].widget.attrs['disabled'] = True
            self.fields['email_address_epa'].required = False
            self.fields['mail_to_zipcode'].widget.attrs['disabled'] = True
            self.fields['mail_to_zipcode'].required = False

            self.fields['agreement_number'].widget.attrs['disabled'] = True
            self.fields['agreement_number'].required = False
            self.fields['agreement_title'].widget.attrs['disabled'] = True
            self.fields['agreement_title'].required = False

    company = forms.CharField(label=_("Organization Name"), widget=forms.TextInput(attrs={'class':'form-control search'}), required=True)
    mail_to_name = forms.CharField(label=_("Contact Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    mail_to_address = forms.CharField(label=_("Address"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    mail_to_city = forms.CharField(label=_("City"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

    mail_to_state = forms.CharField(label=_("State"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    mail_to_zipcode = forms.CharField(label=_("ZIP Code"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    email_address_epa = forms.CharField(label=_("Email"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

    agreement_number = forms.CharField(label=_("Vehicle Number"), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, help_text="For Contract/Grant/Cooperative Agreements")
    agreement_title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, help_text="Common Contract Name")


    class Meta:
        model = ParticipatingOrganization
        fields = ("company", "mail_to_name", "mail_to_address", "mail_to_city", "mail_to_state", "mail_to_zipcode", "email_address_epa", "agreement_number", "agreement_title")


# Commented out to check it's not in use
# class ProjectRequestForm(forms.ModelForm):
#     """
#     A Form For Creating an Project
#     """
#     required_css_class = 'required'
#
#     def __init__(self, *args, **kwargs):
#         super(ProjectRequestForm, self).__init__(*args, **kwargs)
#
#         activpoc_id = self.instance.technical_lead_id
#         self.fields['technical_lead'].queryset = User.objects.filter(
#             Q(userprofile__display_in_dropdowns="Y") | Q(id=activpoc_id)).order_by('last_name', 'first_name', 'email')
#
#
#     date_submitted = forms.CharField(label=_("Date Submitting"), widget=forms.TextInput(attrs={'id':'datepicker1'}), required=False)
#     technical_lead = forms.ModelChoiceField(label=_("Technical Lead"),
#                                             #queryset=User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email'),
#                                             queryset=User.objects.none(),
#                                             widget=forms.Select(), required=False)
#     product_title = forms.CharField(label=_("Product Title"), widget=forms.TextInput(), required=False)
#     project_log_type = forms.ModelChoiceField(label=_("QA Activity"), queryset=ProjectLogType.objects.all(), widget=forms.Select(), required=False)
#     product_type_other = forms.CharField(label=_("Product Type Other"), widget=forms.Textarea, required=False)
#
#     date_review_requested_by = forms.CharField(label=_("Date Review Requested By"), widget=forms.TextInput(attrs={'id':'datepicker2'}), required=False)
#     was_qapp_required = forms.ChoiceField(label=_("Was QAPP Required"), choices=YN_CHOICES, widget=forms.Select(), required=False)
#     was_qapp_prepared = forms.ChoiceField(label=_("Was QAPP Prepared and Approved"),choices=YN_CHOICES, widget=forms.Select(), required=False)
#     project_qa_id = forms.CharField(label=_("Project QA ID"), widget=forms.TextInput(), required=False)
#
#     project_approval_date = forms.CharField(label=_("QA Approval Date"), widget=forms.TextInput(attrs={'id':'datepicker3'}), required=False)
#     qapp_status_explanation = forms.CharField(label=_("If no explain"), widget=forms.Textarea(), required=False)
#     dqi_met = forms.ChoiceField(label=_("DQI Met"), choices=YN_CHOICES, widget=forms.Select(), required=False)
#     dqi_met_some = forms.ChoiceField(label=_("DQA Met Some No data affected"), choices=YN_CHOICES, widget=forms.Select(), required=False)
#
#     dqi_met_some_bad_data = forms.ChoiceField(label=_("DQI Met Bad Data"), choices=YN_CHOICES, widget=forms.Select(), required=False)
#     dqi_na = forms.ChoiceField(label=_("NA"), choices=YN_CHOICES, widget=forms.Select(), required=False)
#     dqi_explanation = forms.CharField(label=_("If no explain"), widget=forms.Textarea(), required=False)
#     electronic_signature = forms.CharField(label=_("Electronic Signature"), widget=forms.TextInput(), required=False)
#
#     date_electronic_signature = forms.CharField(label=_("Electronic Signature Date"), widget=forms.TextInput(attrs={'id':'datepicker4'}), required=False)
#     email_list = forms.CharField(label=_("Email List"), widget=forms.TextInput(), required=False)
#
#     class Meta:
#         model = ProjectRequest
#         fields = ("date_submitted", "technical_lead", "product_title", "project_log_type", "product_type_other", "date_review_requested_by",  "was_qapp_required", "was_qapp_prepared",
#         "project_qa_id", "project_approval_date", "qapp_status_explanation", "dqi_met", "dqi_met_some", "dqi_met_some_bad_data", "dqi_na", "dqi_explanation",
#         "electronic_signature", "date_electronic_signature", "electronic_signature_title", "email_list")

