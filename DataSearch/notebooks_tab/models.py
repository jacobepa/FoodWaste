from django.db import models
import organization.models as org
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.postgres.fields import ArrayField
import projects.models as proj
import datetime
from constants.models import *
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

def get_nbtab_attachment_storage_path(instance, filename):
    return 'nb_tab/%s/%s' % (instance.nbtab_id, filename)

def get_review_attachment_storage_path(instance, filename):
    return 'nb_reviews/%s/%s' % (instance.review_id, filename)

def get_nbtab_attachment_icon(attachment):
    if str(attachment).endswith('pdf'):
        icon_src = settings.STATIC_URL + "img/pdf-icon.jpg"
    elif str(attachment).endswith('xls'):
        icon_src = settings.STATIC_URL + "img/xlsx.jpg"
    elif str(attachment).endswith('xlsx'):
        icon_src = settings.STATIC_URL + "img/xlsx.jpg"
    elif str(attachment).endswith('doc'):
        icon_src = settings.STATIC_URL + "img/word.png"
        icon_src = settings.STATIC_URL + "img/word.png"
    elif str(attachment).endswith('docx'):
        icon_src = settings.STATIC_URL + "img/docx.png"
    elif str(attachment).endswith('doc'):
        icon_src = settings.STATIC_URL + "img/docx.png"
    elif str(attachment).endswith('html'):
        icon_src = settings.STATIC_URL + "img/html.png"
    elif str(attachment).endswith('txt'):
        icon_src = settings.STATIC_URL + "img/txt.jpg"
    elif str(attachment).endswith('csv'):
        icon_src = settings.STATIC_URL + "img/csv.png"
    elif str(attachment).endswith('psd'):
        icon_src = settings.STATIC_URL + "img/psd.jpg"
    else:
        icon_src = settings.STATIC_URL + "uploads/" + str(attachment)
    return icon_src

class NotebooksTab_Type(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['the_name', ]

    def __str__(self):
        return self.the_name or ''


class NotebooksTab_Status(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number', ]

    def __str__(self):
        return self.the_name or ''

class NotebooksTab_NotebookStatus(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number', ]

    def __str__(self):
        return self.the_name or ''


class NotebooksTab(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="nbtab_users")

    previous_id = models.CharField(blank=True, null=True, max_length=255)

    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)

    nb_number = models.CharField(blank=True, null=True, max_length=255)
    alt_id = models.CharField(blank=True, null=True, max_length=255)
    title = models.TextField(null=True, blank=True)
    custodian = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='nb_custodians')
    ord_contributors = models.ManyToManyField(User, related_name='nb_ord_contributors', blank=True)
    non_ord_contributors = models.TextField(blank=True, null=True, db_index=True)
    nb_review_distribution_list = models.ManyToManyField(User, related_name='nb_review_distribution_list', blank=True)
    nb_review_email_list = models.TextField(blank=True, null=True, db_index=True)
    eNotebook_url = models.TextField(null=True, blank=True)
    nb_type = models.ForeignKey(NotebooksTab_Type, on_delete=models.CASCADE, null=True, blank=True)
    qa_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='nbtab_qa_managers')
    supervisor_mentor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='nbtab_supervisors')
    date_issued = models.DateField(null=True, blank=True, db_index=True)
    date_final_use = models.DateField(null=True, blank=True, db_index=True)
    date_archived = models.DateField(null=True, blank=True, db_index=True)
    projects = models.ManyToManyField(proj.Project, blank=True)
    programs = models.ManyToManyField(proj.Program, blank=True)
    participating_orgs = models.ManyToManyField(proj.ParticipatingOrganization, blank=True)
    comments = models.TextField(null=True, blank=True)
    status = models.ForeignKey(NotebooksTab_NotebookStatus, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nb_number or ''


class NBReminder(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    date_email_sent = models.DateTimeField(default=timezone.now, null=True, blank=True)
    nbtab = models.ForeignKey(NotebooksTab, on_delete=models.CASCADE, null=True, blank=True)

    to_email_list = models.TextField(blank=True, null=True, db_index=True)


class NotebooksTabReviewDistribution(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nbtab = models.ForeignKey(NotebooksTab, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["modified",]

    def __str__(self):
        return self.the_name or ''

    def cst(self):
        return self.modified - datetime.timedelta(hours=5)


class NotebooksTab_Orgs(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)

    nbtab = models.ForeignKey(NotebooksTab, on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['nbtab_id', ]

    def __str__(self):
        # Return the abbreviation for the lowest level of organization that is not empty.
        if self.branch is not None:
            return str(self.branch)
        if self.division is not None:
            return str(self.division)
        if self.lab is not None:
            return str(self.lab)

        return str(self.office)


class NotebooksTabAttachment(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, max_length=255,
                                  upload_to=get_nbtab_attachment_storage_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nbtab = models.ForeignKey(NotebooksTab, on_delete=models.CASCADE, null=True, blank=True, related_name="nbtab_attachments")

    include_in_email = models.CharField(default='N', max_length=4, choices=YN_CHOICES)
    is_review_file = models.CharField(default='N', max_length=4, choices=YN_CHOICES)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    the_size = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        ordering = ['the_name', ]

    def icon_to_use(self):
        return get_nbtab_attachment_icon(self.attachment)





class NotebooksTab_approval_history(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="nbhist_users")

    nbtab = models.ForeignKey(NotebooksTab, on_delete=models.CASCADE, null=True, blank=True)

    date_reviewed = models.DateField(null=True, blank=True, db_index=True)
    custodian = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='nbhist_contacts')
    qa_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='nbhist_approving_managers')
    supervisor_mentor =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='nbhist_supervisor_mentor')
    comments = models.TextField(null=True, blank=True)
    nb_status = models.ForeignKey(NotebooksTab_Status, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(NotebooksTab_NotebookStatus, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['id', ]

class NotebooksTab_Reviews(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    nbtab = models.ForeignKey(NotebooksTab, null=True, blank=True, on_delete=models.CASCADE)
    status = models.ForeignKey(NotebooksTab_Status, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateField(default=timezone.now, null=True, blank=True)
    date_reviewed = models.DateField(null=True, blank=True, db_index=True)
    reviewer = models.ForeignKey(User, null=True, blank=True, related_name='reviewer', on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['-date_reviewed']

class NotebooksTab_Schedule_Review(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    nbtab = models.ForeignKey(NotebooksTab, null=True, blank=True, on_delete=models.CASCADE)
    schedule_review = models.CharField(max_length=4, default='N', null=False, blank=True)
    email_last_sent = models.DateField(null=True, blank=True, db_index=True)

class NotebooksTab_Recent_Reviews(models.Model):
#    id  = models.BigIntegerField(primary_key=True)
    user  = models.ForeignKey(blank=False, to=settings.AUTH_USER_MODEL, null=False, on_delete=models.DO_NOTHING)
    review  = models.ForeignKey(NotebooksTab_Reviews, null=True, blank=True, on_delete=models.DO_NOTHING)
    nbtab  = models.ForeignKey(NotebooksTab, null=True, blank=True, on_delete=models.DO_NOTHING)
    status  = models.ForeignKey(NotebooksTab_Status, null=True, blank=True, on_delete=models.DO_NOTHING)
    date_reviewed  = models.DateField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = "notebooks_tab_notebookstab_recent_reviews"

class NotebooksTab_Recent_Emails(models.Model):
#    id  = models.BigIntegerField(primary_key=True)
    user  = models.ForeignKey(blank=False, to=settings.AUTH_USER_MODEL, null=False, on_delete=models.DO_NOTHING)
    review  = models.ForeignKey(NotebooksTab_Reviews, null=True, blank=True, on_delete=models.DO_NOTHING)
    nbtab  = models.ForeignKey(NotebooksTab, null=True, blank=True, on_delete=models.DO_NOTHING)
    email_last_sent  = models.DateField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = "notebooks_tab_notebookstab_recent_emails"


class NotebooksTab_User_Notebooks(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.DO_NOTHING)
    nbtab_ids = ArrayField(base_field=models.IntegerField(), size=None)
    roles = ArrayField(base_field=models.TextField(), size=None)
    review_ids = ArrayField(base_field=models.IntegerField(), size=None)
    recent_review = models.ForeignKey(NotebooksTab_Recent_Reviews, null=True, blank=True, on_delete=models.DO_NOTHING)
    recent_email = models.ForeignKey(NotebooksTab_Recent_Emails, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "notebooks_tab_notebookstab_user_notebooks"

class NotebooksTabReviewAttachment(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, max_length=255,
                                  upload_to=get_review_attachment_storage_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(NotebooksTab_Reviews, on_delete=models.CASCADE, null=True, blank=True, related_name="nb_review_attachments")

    include_in_email = models.CharField(default='N', max_length=4, choices=YN_CHOICES)
    is_review_file = models.CharField(default='N', max_length=4, choices=YN_CHOICES)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    the_size = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        ordering = ['the_name', ]

    def icon_to_use(self):
        return get_nbtab_attachment_icon(self.attachment)

@receiver(post_delete, sender=NotebooksTabReviewAttachment)
def photo_post_delete_handler(sender, **kwargs):
    pa = kwargs['instance']
    storage, path = pa.attachment.storage, pa.attachment.path
    storage.delete(path)
