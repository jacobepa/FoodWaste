#
# Models representing the organizational structure of the EPA
# Research Management System (RMS)
#
# Program - RMS program
# Project - RMS project, NOT the same as a QA Track project!!
# Task - RMS Task
#

from django.db import models
from DataSearch import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

def get_project_attachment_storage_path(instance, filename):
    print("Getting storage path")
    return 'RMSproject/%s/%s' % (instance.project_id, filename)


class Program(models.Model):
    """
    EPA RMS Program
    """
    title = models.CharField(blank=False, max_length=255)
    acronym = models.CharField(blank=False, max_length=32)

    url = models.CharField(blank=True, null=True, max_length=1024)
    # id from RMs database
    rms_id = models.IntegerField(null=False, unique=True)

    show_projects = models.BooleanField(default=True, null=False)

    # Commented out - seemed unnecessary since was just returning pass.
    # Was causing error to show project in Django admin tool.
    #def __str__(self):
        # return self.acronym
    #    pass


class Project(models.Model):
    """
    EPA RMS Project
    """
    title = models.CharField(blank=False, max_length=255)
    epa_id = models.CharField(blank=False, max_length=32)
    IRMS_project_id = models.CharField(blank=True,null=True, max_length=32)
    # foreign key from RMs database
    RMSprogram_id = models.IntegerField(null=False)

    url = models.CharField(blank=True, null=True, max_length=1024)
    # id from RMs database
    rms_id = models.IntegerField(null=False, unique=True)

    # program containing this project
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    start_date = models.CharField(blank=True, null=True, max_length=32)
    end_date = models.CharField(blank=True, null=True, max_length=32)

    def __str__(self):
        return self.program.acronym + " - " + self.title or ''

    class Meta:
        ordering = ['epa_id']

class Task(models.Model):
    """
    EPA RMS Task
    """
    title = models.CharField(blank=False, max_length=512)
    epa_id = models.CharField(blank=False, max_length=32)
    # foreign key from RMs database
    RMSproject_id = models.IntegerField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    url = models.CharField(blank=True, null=True, max_length=1024)
    # id from RMs database
    rms_id = models.IntegerField(null=False)

    start_date = models.CharField(blank=True, null=True, max_length=32)
    end_date = models.CharField(blank=True, null=True, max_length=32)

    def __str__(self):
        return self.program.acronym + ' ' + self.epa_id + ' ' + self.title or ''

    class Meta:
        ordering = ['epa_id']

class RMSProjectAttachment(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    attachment = models.FileField(null=True, blank=True, max_length=255, upload_to=get_project_attachment_storage_path)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    file_name = models.CharField(blank=True, null=True, max_length=255)
    file_size = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        ordering = ['file_name']

    def icon_to_use(self):
        if str(self.attachment).endswith('pdf'):
            icon_src = settings.STATIC_URL + "img/pdf-icon.jpg"
        elif str(self.attachment).endswith('xls'):
            icon_src = settings.STATIC_URL + "img/xlsx.jpg"
        elif str(self.attachment).endswith('xlsx'):
            icon_src = settings.STATIC_URL + "img/xlsx.jpg"
        elif str(self.attachment).endswith('doc'):
            icon_src = settings.STATIC_URL + "img/word.png"
        elif str(self.attachment).endswith('docx'):
            icon_src = settings.STATIC_URL + "img/docx.png"
        elif str(self.attachment).endswith('doc'):
            icon_src = settings.STATIC_URL + "img/docx.png"
        elif str(self.attachment).endswith('html'):
            icon_src = settings.STATIC_URL + "img/html.png"
        elif str(self.attachment).endswith('txt'):
            icon_src = settings.STATIC_URL + "img/txt.jpg"
        elif str(self.attachment).endswith('csv'):
            icon_src = settings.STATIC_URL + "img/csv.png"
        elif str(self.attachment).endswith('psd'):
            icon_src = settings.STATIC_URL + "img/psd.jpg"
        else:
            icon_src = settings.STATIC_URL + "uploads/" + str(self.attachment)
        return icon_src



@receiver(post_delete, sender=RMSProjectAttachment)
def photo_post_delete_handler(sender, **kwargs):
    pa = kwargs['instance']
    storage, path = pa.attachment.storage, pa.attachment.path
    storage.delete(path)
