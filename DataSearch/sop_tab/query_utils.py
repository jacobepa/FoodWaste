#
# This file defines some utilities for querying disciplines and subdisciplines
#
#
from django.db.models import Q
from sop_tab.models import *
import json

def get_discipline_list(as_json=False, include_inactive=False):
    """
    Get the list of disciplines
    :param:
    :return:
    """

    # Sort by sort_number.
    if include_inactive:
        discipline_list = Discipline.objects.order_by('sort_number').all()
    else:
        discipline_list = Discipline.objects.filter(is_active="Y").order_by('sort_number')

    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "discipline": obj.discipline}
                           for obj in discipline_list])
    else:
        return discipline_list

def get_subdiscipline_list(discipline=None, as_json=False, include_inactive=False):
    """
    Get the list of subdisciplines
    :param:
    :return:
    """

    # Sort alphabetically by name of subdiscipline.
    if discipline is None:
        if include_inactive:
            subdiscipline_list = (
                SubDiscipline.objects
                    .order_by('subdiscipline')
                    .select_related("discipline")
                    .all()
            )
        else:
            subdiscipline_list = (
                SubDiscipline.objects
                    .order_by('subdiscipline')
                    .select_related("discipline")
                    .filter(is_active="Y")
            )
    else:
        if include_inactive:
            subdiscipline_list = (
                SubDiscipline.objects.filter(discipline=discipline)
                    .order_by('subdiscipline')
                    .select_related("discipline")
                    .all()
            )
        else:
            subdiscipline_list = (
                SubDiscipline.objects.filter(discipline=discipline)
                    .order_by('subdiscipline')
                    .select_related("discipline")
                    .filter(is_active="Y")
            )


    if as_json:
        return json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "subdiscipline": obj.subdiscipline,
                            "discipline_id": obj.discipline.id }
                           for obj in subdiscipline_list])
    else:
        return subdiscipline_list
