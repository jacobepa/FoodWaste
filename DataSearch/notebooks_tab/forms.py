from django import forms
from django.forms import widgets, ModelForm, ValidationError
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectDateWidget

from constants.models import *
from constants.utils import *

from notebooks_tab.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.db.models import Q
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from projects.models import *
from organization.models import *
from datetime import datetime
from collections import OrderedDict

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name + " (" + obj.email + ")"

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name + " (" + obj.email + ")"

class ProjectModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Add project title to label in dropdown if there is one.
        if obj.title:
            label_idtitle = obj.qa_id + " " + obj.title
        else:
            label_idtitle = obj.qa_id
        return label_idtitle

# # # # # # #
#
# NOTEBOOKS TAB FORM ASYNC
#
# # # # # # #
class NotebooksTabFormAsync(forms.ModelForm):

    required_css_class = 'required'

    previous_id = forms.CharField(label=_("Previous ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                             required=False,
                             help_text="The previous ID can be used for any ID the Notebook was assigned by EPA prior to being entered in or imported to QA Track.")

    alt_id = forms.CharField(label=_("Alternate ID"), widget=forms.TextInput(attrs={"class": "form-control"}),
                             required=False,
                             help_text="The alternate ID can be used for a number from another system.")

    title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={"class": "form-control"}), required=True,
                        help_text = "Enter the title as it appears on the hardcopy cover or to match the title in OneNote.")

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    custodian = UserModelChoiceField(label=_("Notebook Custodian"),

                                     queryset=User.objects.none(),
                                     empty_label="",
                                     widget=forms.Select(attrs={"class": "form-control jasc-user-select",
                                                                "data-placeholder": "Search people..."}),
                                     required=True,
                                     help_text="")

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    ord_contributors = UserModelMultipleChoiceField(label=_("Contributors"),
                                                    widget=forms.SelectMultiple(
                                                        attrs={'class': 'form-control jasc-user-select',
                                                               'data-placeholder': 'Search people . . .'}),
                                                    queryset=User.objects.none(),
                                                    required=False,
                                                    help_text='')

    non_ord_contributors = forms.CharField(label=_("Non-ORD Contributors"),
                                       widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                                       help_text='Enter emails separated by whitespace')

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    nb_review_distribution_list = UserModelMultipleChoiceField(label=_("Notebook Correspondence Email List (ORD)"),
                                                                  widget=forms.SelectMultiple(
                                                                      attrs={'class': 'form-control jasc-user-select',
                                                                             'data-placeholder': 'Search people . . .'}),
                                                                  queryset=User.objects.none(),
                                                                  required=False,
                                                                  help_text='')

    nb_review_email_list = forms.CharField(label=_("Email List (non-ORD, separated by whitespace)"),
                                          widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                                          help_text='')

    eNotebook_url = forms.CharField(label=_("Electronic Notebook URL"), widget=forms.Textarea(attrs={'class': 'form-control'}),
                               required=False)

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


    nb_type = forms.ModelChoiceField(label=_("Notebook Type"),
                          queryset=NotebooksTab_Type.objects.filter(is_active="Y").order_by('sort_number'),
                          widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    status = forms.ModelChoiceField(label=_("Status"),
                                       queryset=NotebooksTab_NotebookStatus.objects.filter(is_active="Y"),
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    qa_manager = UserModelChoiceField(label=_("QA Manager"),
                                      queryset=User.objects.none(),
                                      empty_label="",
                                                  widget=forms.Select(attrs={"class": "form-control jasc-user-select",
                                                                             "data-placeholder": "Search people..."}),
                                                  required=True,
                                                  help_text="")

    #
    # API: User.objects.filter(userprofile__display_in_dropdowns="Y").order_by('last_name', 'first_name', 'email')
    #
    supervisor_mentor = UserModelChoiceField(label=_("Supervisor/Mentor"),
                                     queryset=User.objects.none(),
                                     empty_label="",
                                      widget=forms.Select(attrs={"class": "form-control jasc-user-select",
                                                                 "data-placeholder": "Search people..."}),
                                      required=True,
                                      help_text="")

    date_issued = forms.DateField(label=_("Date Issued"),
                                    widget=forms.TextInput(attrs={'class': 'form-control date-control'}),
                                    required=True)

    date_final_use = forms.DateField(label=_("Date of Final Use"),
                                  widget=forms.TextInput(attrs={'class': 'form-control date-control'}),
                                  required=False)

    date_archived = forms.DateField(label=_("Date Archived"),
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
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control jasc-program-select',
                                                                          'data-placeholder': 'Search programs . . .'}),
                                              queryset=Program.objects.none(), required=False)

    #
    # API: ParticipatingOrganization.objects.none().order_by('company')
    #
    participating_orgs = forms.ModelMultipleChoiceField(label=_("EPA Non-ORD Organizations"), widget=forms.SelectMultiple(
        attrs={'class': 'form-control jasc-org-select',
               'data-placeholder': 'Search non-ORD orgs . . .'}),
                                               queryset=ParticipatingOrganization.objects.none(),
                                               required=False)

    comments = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={'class': 'form-control'}),
                               required=False)

    def __init__(self, *args, **kwargs):
        super(NotebooksTabFormAsync, self).__init__(*args, **kwargs)

        async_filters = {
            "custodian": (User, Q(userprofile__display_in_dropdowns="Y")),
            "ord_contributors": (User, Q(userprofile__display_in_dropdowns="Y")),
            "qa_manager": (User, Q(userprofile__display_in_dropdowns="Y")),
            "supervisor_mentor": (User, Q(userprofile__display_in_dropdowns="Y")),
            "projects": (Project, True),
            "programs": (Program, Q(is_active="Y")),
            "participating_orgs": (ParticipatingOrganization, True),
            "nb_review_distribution_list": (User, Q(userprofile__display_in_dropdowns="Y"))
        }

        setQuerySets(self, async_filters, kwargs)


    def clean(self):
        form_data = self.cleaned_data
        email_list = split_email_list(form_data['nb_review_email_list'])
        bad_emails = []
        for email in email_list:
            if not is_epa_email(email):
                bad_emails.append(email)
        if len(bad_emails):
            raise ValidationError({'nb_review_email_list':[non_epa_email_message(bad_emails),]})
        return form_data

    class Meta:
        model = NotebooksTab
        fields = (
                "office",
                "lab",
                "division",
                "branch",
                "title",
                "comments",
                "nb_type",
                "status",
                "alt_id",
                "previous_id",
                "eNotebook_url",
                "custodian",
                "ord_contributors",
                "non_ord_contributors",
                "qa_manager",
                "supervisor_mentor",
                "date_issued",
                "date_final_use",
                "date_archived",
                "projects",
                "programs",
                "participating_orgs",
                "nb_review_distribution_list",
                "nb_review_email_list",
                )


class NotebooksTabReviewFormAsync(forms.ModelForm):

    required_css_class = 'required'

    nb_user = UserModelChoiceField(label=_("Custodian/Contributor"), queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control chosen-select'}), required=True)
    notebook = forms.ModelChoiceField(label=_("Notebook"), queryset=NotebooksTab.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    date_reviewed = forms.DateField(label=_("Review Date"), widget=forms.TextInput(attrs={'class': 'form-control date-control'},), required=True)
    status = forms.ModelChoiceField(label=_("Review Status"), queryset=NotebooksTab_Status.objects.filter(is_active="Y").order_by('id'), widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    reviewer = UserModelChoiceField(label=_("Reviewed by"), queryset=User.objects.none(), empty_label="",
            widget=forms.Select(attrs={"class": "form-control jasc-user-select", "data-placeholder": "Search people..."}), required=True, help_text="")
    comments = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    def __init__(self, user_id=0, nb_id=0, editing=False,  *args, **kwargs):
        super(NotebooksTabReviewFormAsync, self).__init__(*args, **kwargs)

        user_id = int(user_id)
        nb_id = int(nb_id)

#        print(self.instance.pk)
#        if user_id != 0 and user_id is not None and nb_id != 0 and nb_id is not None:
#        if self.instance.pk is not None: # editing a record
        if editing:
            notebooks = NotebooksTab.objects.filter(pk=nb_id)
            nb = notebooks.first()
            users = User.objects.filter(pk=user_id)
            user = users.first()
            self.fields['notebook'] = forms.CharField(label=_("Notebook"), widget=forms.TextInput(attrs={"class": "form-control","readonly":True, "value": nb.nb_number}))
            self.fields['nb_user'] = forms.CharField(label=_("Custodian/Contributor"), widget=forms.TextInput(attrs={"class": "form-control","readonly":True, "value": user.userprofile.r_name}))


        else:

            #
            # If a user_id is provided, freeze the user
            #
            if user_id != 0 and user_id is not None:
                user_nbs = NotebooksTab_User_Notebooks.objects.filter(user_id=user_id).first()
                nb_ids = [int(_id) for _id in user_nbs.nbtab_ids] if user_nbs is not None else []
                self.fields['notebook'].queryset = NotebooksTab.objects.filter(pk__in=nb_ids)
                self.fields['nb_user'].queryset = User.objects.filter(pk=user_id)
                self.fields['nb_user'].initial = user_id
                self.fields['nb_user'].empty_label = None

                notebooks = NotebooksTab.objects.filter(pk__in=nb_ids)

            #
            # elif a nb_id is provided, freeze the notebook
            #
            elif nb_id != 0 and nb_id is not None:
                nb_users = NotebooksTab_User_Notebooks.objects.filter(nbtab_ids__contains=[nb_id])

                user_ids = [u.user_id for u in nb_users]
                self.fields['nb_user'].queryset = User.objects.filter(pk__in=user_ids)
                if len(user_ids) == 1:
                    self.fields['nb_user'].initial = user_ids[0]

                self.fields['notebook'].queryset = NotebooksTab.objects.filter(pk=nb_id)
                self.fields['notebook'].initial = nb_id
                self.fields['notebook'].empty_label = None

                self.field_order = [ 'notebook', 'nb_user' ,'date_reviewed','status','reviewer','comments']
                self.fields = OrderedDict((k, self.fields[k]) for k in self.field_order)

                notebooks = NotebooksTab.objects.filter(pk=nb_id)

            default_date = datetime.today().strftime('%Y-%m-%d')
            self.fields['date_reviewed'].initial = default_date


        qam_nbs = notebooks.filter(qa_manager__isnull=False)
        qam_ids = [ nb.qa_manager.id for nb in qam_nbs ]
        mentor_nbs = notebooks.filter(supervisor_mentor__isnull=False)
        mentor_ids = [ nb.supervisor_mentor.id for nb in mentor_nbs ]
        self.fields['reviewer'].queryset = User.objects.filter(
                (Q(userprofile__display_in_dropdowns="Y") #& Q(userprofile__is_reviewer="Y")
                    )
                | Q(id__in=qam_ids)
                | Q(id__in=mentor_ids)
            ).order_by('last_name', 'first_name', 'email')


        if notebooks.count() == 1 and len(qam_ids) == 1:
            self.fields['reviewer'].initial = qam_ids[0]





    class Meta:
        model = NotebooksTab_Reviews
        fields = ("nb_user","notebook","date_reviewed","status","reviewer","comments")

