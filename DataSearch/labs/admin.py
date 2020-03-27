from django.contrib import admin

from labs.models import *
		
# class LabAdmin(admin.ModelAdmin):
#     list_display = ("abbreviation", "the_name", "weblink")
#     search_fields = ("abbreviation", "the_name", )
#     exclude = ('created_by', 'last_modified_by',)
#     list_filter = ("abbreviation", "the_name", )
#     list_per_page = 25
#
# admin.site.register(Lab, LabAdmin)
