#
# This file defines some utilities for querying the EPA organizational
# structure
#
#
from django.db.models import Q
from organization.models import *
import json

def get_office_list(user, as_json=False):
    """
    Get the list of offices that this user can view
    :param user:
    :return:
    """
    try:
        userprofile = user.userprofile
        user_perm = userprofile.permissions
#        user_type = userprofile.user_type
#        if user_type == "SUPER" or user_type == "OFFICE" or user_type == "ALL":
        if user_perm == 'ADMIN':
            office_list = Office.objects.order_by('abbreviation').all()
        else:
            # See only your ofice.
            if userprofile.office is not None:
                office_list = [userprofile.office]
            else:
                office_list = []
    except:
        office_list = []

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "office": obj.office}
                           for obj in office_list])
    else:
        return office_list

# Get unrestricted list of offices.
def get_unrestricted_office_list(user, as_json=False):
    """
    Get the list of offices that this user can view
    :param user:
    :return:
    """
    try:
        office_list = Office.objects.order_by('abbreviation').all()

    except:
        office_list = []

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "office": obj.office}
                           for obj in office_list])
    else:
        return office_list

def get_lab_list(user, office=None, as_json=False, include_labs=[]):
    """
    Get the list of labs that this user can view
    :param user: User model object.
    :param include_labs: Force include some labs, used in case of allowing editors to edit
    any qa activity of a project in their org (the qa activity might have a different org).
    :return: list of Lab model objects
    """

    # ALERT: If you make changes here, also change it in organization/query_utils.py
    # Method to allow QAMs to edit records under their old orgs.
    oldlabs = {
        'libby415': 12,
        'svandegr': 12,
        'JohnOlszewski': 12,
        'jhoelle-schwalbach': 12,
        'mbob': 12,
        'kschrantz': 12,
        'jvoit': 12,
        'dyoung11': 12,
        'RobertSWright': 12,
        'rsherm01': 14,
        'ebrady': 14,
        'citkin': 8,
        'srober03': 5,
        'ldoucet': 13,
        'bstuart': 10,
        'stong02': 10,
        'calvar02': 10,
        'mvazquez': 10,
        'jnoel02': 10,
        'mhenders': 10,
        'kgarcia': 10,
        'abaxte04': 10,
        'jpancras': 9,
        'jmarkwie': 9,
        'jlivolsi': 9,
        'jscott07': 9,
        'awatkins': 9,
        'gnelson': 9,
        'bsheedy': 9,
        'jberninger': 9,
        'dandrews': 9,
        'hferguson': 9,
        'kjarema': 9,
        'janetest': 9
    }

    if user is None:
        return []
    try:
        userprofile = user.userprofile
#        user_type = userprofile.user_type
        user_perm = userprofile.permissions

        if user.username in oldlabs:
            oldlab = oldlabs[user.username]
            include_labs.append(oldlab)
        else:
            oldlab = None

        if user_perm == 'ADMIN':
            if office is None:
                lab_list = list(
                    Lab.objects.exclude(designation_code__isnull=True)
                        .order_by('abbreviation')
                        .select_related("office")
                        .all()
                )
            else:
                lab_list = list(
                    Lab.objects.filter(office=office).exclude(designation_code__isnull=True)
                        .order_by('abbreviation')
                        .select_related("office")
                        .all()
                )
        else:
            # EDITORs and READERs only see their lab.
            if userprofile.lab is not None:
                lab_list = [userprofile.lab]
            else:
                lab_list = []
    except:
        lab_list = []

    #Add include_labs:
    if len(include_labs) > 0:
        lab_list = list(set(lab_list + list(Lab.objects.filter(pk__in=include_labs))))

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "lab": obj.lab,
                            "office_id": obj.office.id, "is_active": obj.is_active }
                           for obj in lab_list])
    else:
        return lab_list

# Get unrestricted list of labs.
def get_unrestricted_lab_list(user, office=None, as_json=False):
    """
    Get the list of labs according to office
    :param user:
    :return:
    """

    try:
        if office is None:
            lab_list = (
                Lab.objects.exclude(designation_code__isnull=True)
                    .order_by('abbreviation')
                    .select_related("office")
                    .all()
            )
        else:
            lab_list = (
                Lab.objects.filter(office=office).exclude(designation_code__isnull=True)
                    .order_by('abbreviation')
                    .select_related("office")
                    .all()
            )
    except:
        lab_list = []

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "lab": obj.lab,
                            "office_id": obj.office.id, "is_active": obj.is_active }
                           for obj in lab_list])
    else:
        return lab_list

def get_division_list(user, office=None, lab=None, as_json=False):
    """
    Get the list of divisions that this user can view
    :param user:
    :return:
    """
    if user is None:
        return []

    try:
        userprofile = user.userprofile
#        user_type = userprofile.user_type
        query = Q()
        if office is not None:
            query = Q(office = office)
        if lab is not None:
            query = query & Q(lab = lab)

        division_list = (
            Division.objects.filter(query).order_by('abbreviation')
                .select_related("lab", "office")
                .all()
        )
    except:
        division_list = []

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "division": obj.division,
                            "lab_id": obj.lab.id, "office_id": obj.office.id, "is_active": obj.is_active}
                           for obj in division_list])
    else:
        return division_list

# Get unrestricted list of divisions.
def get_unrestricted_division_list(user, office=None, lab=None, as_json=False):
    """
    Get the list of divisions according to office and lab selection.
    :param user:
    :return:
    """

    try:
        query = Q()
        if office is not None:
            query = Q(office = office)
        if lab is not None:
            query = query & Q(lab = lab)

        division_list = (
            Division.objects.filter(query).order_by('abbreviation')
                .select_related("lab", "office")
                .all()
        )

    except:
        division_list = []

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "division": obj.division,
                            "lab_id": obj.lab.id, "office_id": obj.office.id, "is_active": obj.is_active}
                           for obj in division_list])
    else:
        return division_list

def get_branch_list(user, office, lab, division, as_json=False):
    """
    Get the list of branches that this user can view
    :param user:
    :param office:
    :param lab:
    :param division:
    :return:
    """
    if user is None:
        return []

    try:
        userprofile = user.userprofile
#        user_type = userprofile.user_type


        query = Q()
        if office is not None:
            query = Q(office = office)
        if lab is not None:
            query = query & Q(lab = lab)
        if division is not None:
            query = query & Q(division = division)
        branch_list = (
            Branch.objects.filter(query).order_by('abbreviation')
                .select_related("office", "lab", "division")
                .all()
        )
    except:
        branch_list = []

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "branch": obj.branch,
                            "division_id": obj.division.id, "lab_id": obj.lab.id, "office_id": obj.office.id,
                            "is_active": obj.is_active}
                           for obj in branch_list])
    else:
        return branch_list


# Get unrestricted list of branches.
def get_unrestricted_branch_list(user, office, lab, division, as_json=False):
    """
    Get the list of branches according to office/lab/division selection.
    :param user:
    :param office:
    :param lab:
    :param division:
    :return:
    """

    try:
        query = Q()
        if office is not None:
            query = Q(office = office)
        if lab is not None:
            query = query & Q(lab = lab)
        if division is not None:
            query = query & Q(division = division)
        branch_list = (
            Branch.objects.filter(query).order_by('abbreviation')
                .select_related("office", "lab", "division")
                .all()
        )
    except:
        branch_list = []

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "branch": obj.branch,
                            "division_id": obj.division.id, "lab_id": obj.lab.id, "office_id": obj.office.id,
                            "is_active": obj.is_active}
                           for obj in branch_list])
    else:
        return branch_list


def _valid_org_id(value):
    return (value is not None and value != '')
