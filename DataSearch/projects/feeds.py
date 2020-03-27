from .models import ProjectLog, Project, ProjectAttachment
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
import datetime
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import login_required


class CustomRapidFeedGenerator(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomRapidFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement("qa_category", item['qa_category'])
        handler.addQuickElement("qa_activity_number", item['qa_activity_number'])
        handler.addQuickElement("intramural_extramural", item['intramural_extramural'])
        handler.addQuickElement("project_type", item['project_type'])
        handler.addQuickElement("qapp_status", item['qapp_status'])
        handler.addQuickElement("qapp_approval_date", item['qapp_approval_date'])
        handler.addQuickElement("date_approved", item['date_approved'])
        handler.addQuickElement("qa_activity_poc", item['qa_activity_poc'])
        handler.addQuickElement("qa_activity_poc_email", item['qa_activity_poc_email'])
        handler.addQuickElement("project_lead", item['project_lead'])
        handler.addQuickElement("project_lead_email", item['project_lead_email'])
        handler.addQuickElement("qapp_latest_pdf", item['qapp_latest_pdf'])
        handler.addQuickElement("qapp_latest_word", item['qapp_latest_word'])
        handler.addQuickElement(u"lab", item['lab'])
        handler.addQuickElement(u"division", item['division'])

class LatestRapidQAPPFeed(Feed):
    qapp_title = "Latest Approved QAPP Feed"
    link = settings.MEDIA_URL
    description = "Latest Approved QAPPs"

    feed_type = CustomRapidFeedGenerator

    def items(self):

        query = Q(project_log_type__the_name="QAPP")
        projects = Project.objects.filter(project_status_id=1)
        ids = []
        qapp_query = Q(project_log_type__the_name="QAPP") & Q(date_approved__isnull=False) & ( Q(review_type__the_name="Approved") | Q(review_type__the_name="Approved with minor revisions"))
        for proj in projects:
            proj_qapps = ProjectLog.objects.filter(qapp_query & Q(project=proj))
            if proj_qapps.count() == 0:
                continue
            else:
                sorted_qapps = sorted(proj_qapps,key= lambda qapp:qapp.qa_log_number.split('-')[-1] )
                ids.append(sorted_qapps[-1].id)

        qapps = ProjectLog.objects.filter(id__in=ids).select_related('project')
        for qapp in qapps:
            qapp.restrict_qapp_files = qapp.project.restrict_qapp_files
            latest_pdf = ProjectAttachment.objects.filter(project_id=qapp.project_id,is_latest_qapp_pdf='Y').first()
            qapp.qapp_latest_pdf = self.request.build_absolute_uri(settings.MEDIA_URL + str(latest_pdf.attachment)) if latest_pdf is not None else ""

            latest_word = ProjectAttachment.objects.filter(project_id=qapp.project_id,is_latest_qapp_doc='Y').first()
            qapp.qapp_latest_word = self.request.build_absolute_uri(settings.MEDIA_URL + str(latest_word.attachment)) if latest_word is not None else ""

        return qapps

    def item_title(self, item):
        return item.title

    def item_link(self,item):
        if item.qapp_latest_pdf != "":
            return item.qapp_latest_pdf
        elif item.qapp_latest_word != "":
            return item.qapp_latest_word
        else:
            return "/projects/qlog/show/" + str(item.id)

    def get_object(self, request):
        #Give item_extra_kwargs access to request obj
        self.request = request
        return None

    def item_extra_kwargs(self, obj):

        technical_lead = obj.technical_lead.first_name + " " + obj.technical_lead.last_name if obj.technical_lead is not None else ""
        technical_lead_email = obj.technical_lead.email if obj.technical_lead is not None else ""
        project_lead = obj.project.person.first_name + " " + obj.project.person.last_name if obj.project.person is not None else ""
        project_lead_email = obj.project.person.email if obj.project.person is not None else ""
        intramural_extramural = obj.project.project_type.the_name if obj.project.project_type is not None else ""
        lab = obj.lab.abbreviation if obj.lab else ""
        division = obj.division.abbreviation if obj.division else ""

        project_type = ""
        if obj.project.nrmrl_qapp_requirement is not None:
            for p in obj.project.nrmrl_qapp_requirement.all():
                project_type += p.the_name + ', '
            # Clean up dangling comma.
            last_chars = project_type[len(project_type) - 2:]
            if last_chars == ', ':
                project_type = project_type[:-2]


        return {
                "qa_category": str(obj.project.qa_category),
                "qa_activity_number": str(obj.qa_log_number),
                "intramural_extramural": str(intramural_extramural),
                "project_type": str(project_type),
                "qapp_status": str(obj.project.qapp_status),
                "qapp_approval_date": str(obj.project.qapp_approval_date),
                "date_approved": str(obj.date_approved),
                "qa_activity_poc": str(technical_lead),
                "qa_activity_poc_email": str(technical_lead_email),
                "project_lead": str(project_lead),
                "project_lead_email": str(project_lead_email),
                "qapp_latest_pdf": str(obj.qapp_latest_pdf),
                "qapp_latest_word": str(obj.qapp_latest_word),
                'lab': lab,
                'division': division
                }


#
# This is an extension of the LatestRapidQAPPFeed with projects removed which are marked as restrict_qapp_files==True
#
class LatestORDQAPPFeed(LatestRapidQAPPFeed):
    def items(self, request):
        qapps = super().items()

        # We're sending a list through because for some reason we were lsoing qapp_latest_* on filtering the queryset.
        public_qapps_with_files = []
        for qapp in qapps:
            if (qapp.qapp_latest_word != "" or qapp.qapp_latest_pdf != "" ) and qapp.restrict_qapp_files == False:
                public_qapps_with_files.append(qapp)

        return public_qapps_with_files
