from .models import SOPTab
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
import datetime
from django.conf import settings


class CustomFeedGenerator(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"sop_number", item['sop_number'])
        handler.addQuickElement(u"sop_status", item['sop_status'])
        handler.addQuickElement(u"date_reviewed", item['date_reviewed'])
        handler.addQuickElement(u"discipline", item['discipline'])
        handler.addQuickElement(u"subdiscipline", item['subdiscipline'])
        handler.addQuickElement(u"sop_contact", item['sop_contact'])
        handler.addQuickElement(u"lab", item['lab'])
        handler.addQuickElement(u"division", item['division'])
        handler.addQuickElement(u"previous_id", item['previous_id'])
        handler.addQuickElement(u"alt_id", item['alt_id'])


class LatestSOPFeed(Feed):
    title = "Latest SOPs"
    link = settings.MEDIA_URL
    description = "SOP Numbers"

    feed_type = CustomFeedGenerator

    def items(self):

        # strSQL = (
        # "select sop_info.id, attachment as attachment_path from (select st.id, attachment "
        # "from sop_tab_soptab st "
        # "inner join "
        # "(select soptab_id, attachment, (select sop_base_id from sop_tab_soptab where id = soptab_id) as att_base_id "
        # "from sop_tab_soptabattachment where is_latest_sop = 'Y') at "
        # "on (st.sop_base_id = at.att_base_id) "
        # "where is_current = 'Y' "
        # "and sop_status_id in (select id from sop_tab_soptab_status where the_name in ('Under Review')) "
        # "union "
        # "select st.id, attachment from sop_tab_soptab st "
        # "inner join "
        # "(select soptab_id, attachment from sop_tab_soptabattachment where is_latest_sop = 'Y') at "
        # "on (st.id = at.soptab_id) "
        # "where is_current = 'Y' "
        # "and sop_status_id in (select id from sop_tab_soptab_status where the_name in ('Active'))) sop_info "
        # )

        strSQL = (
        "select soptab_id as id, attachment as attachment_path "
        "from sop_tab_soptab st "
        "inner join "
        "(select soptab_id, attachment, (select sop_base_id from sop_tab_soptab where id = soptab_id) as att_base_id "
        "from sop_tab_soptabattachment where is_latest_sop = 'Y') at "
        "on (st.sop_base_id = at.att_base_id) "
        "where is_current = 'Y' "
        "and sop_status_id in (select id from sop_tab_soptab_status where the_name in ('Under Review')) "
        "union  "
        "select st.id as id, attachment as attachment_path from sop_tab_soptab st "
        "inner join "
        "(select soptab_id, attachment from sop_tab_soptabattachment where is_latest_sop = 'Y') at "
        "on (st.id = at.soptab_id) "
        "where is_current = 'Y'  "
        "and sop_status_id in (select id from sop_tab_soptab_status where the_name in ('Active')) "
        )

        return SOPTab.objects.raw(strSQL)


    def item_title(self, item):
        return item.full_title

    def item_description(self, item):
        return ""

    def item_link(self, item):
        return settings.MEDIA_URL + item.attachment_path


    def item_extra_kwargs(self, obj):
        if obj.date_reviewed:
            date_reviewed = datetime.datetime.strftime(obj.date_reviewed, "%Y-%m-%d")
        elif obj.date_approved:
            date_reviewed = datetime.datetime.strftime(obj.date_approved, "%Y-%m-%d")
        else:
            date_reviewed = ""

        sop_status = obj.sop_status.the_name if obj.sop_status else ""
        discipline = obj.discipline.discipline if obj.discipline else ""
        subdiscipline = obj.subdiscipline.subdiscipline if obj.subdiscipline else ""
        lab = obj.lab.abbreviation if obj.lab else ""
        division = obj.division.abbreviation if obj.division else ""
        sop_contact = obj.sop_contact.first_name + " " + obj.sop_contact.last_name if obj.sop_contact else ""

        return {'sop_number': obj.sop_number,
                'sop_status': sop_status,
                'date_reviewed': date_reviewed,
                'discipline': discipline,
                'subdiscipline': subdiscipline,
                'lab': lab,
                'division': division,
                'previous_id': obj.previous_id,
                'alt_id': obj.alt_id,
                'sop_contact': sop_contact}
