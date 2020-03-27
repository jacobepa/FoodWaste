from django.contrib import admin
from rms.models import *

# Register your models here.


class ProgramAdmin(admin.ModelAdmin):
    list_display = ("acronym", "show_projects")
    list_editable = ("show_projects",)
    list_per_page = 25
    list_display_links = None

#    def __init__(self, *args, **kwargs):
#        super(ProgramAdmin, self).__init__(*args, **kwargs)
#        self.list_display_links = (None, )

admin.site.register(Program, ProgramAdmin )
