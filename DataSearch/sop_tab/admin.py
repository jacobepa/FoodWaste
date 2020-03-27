from django.contrib import admin

from sop_tab.models import *

class SOPAdmin(admin.ModelAdmin):
    list_display = ("sop_number", "full_title", "sop_type", "sop_status","discipline","subdiscipline")
    search_fields = ["sop_number", "full_title",]
    list_filter = ("sop_type", "sop_status","discipline","subdiscipline")
    list_per_page = 25

admin.site.register(SOPTab, SOPAdmin)

class SOPTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(SOPTab_Type, SOPTypeAdmin)

class SOPMuralTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(SOPTab_MuralType, SOPMuralTypeAdmin)

class SOPStatusTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", "sort_number", "is_active",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(SOPTab_Status, SOPStatusTypeAdmin)

class SOPDisciplineAdmin(admin.ModelAdmin):
    list_display = ("discipline", "id", "sort_number", "is_active",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(Discipline, SOPDisciplineAdmin)

class SOPSubdisciplineAdmin(admin.ModelAdmin):
    list_display = ("subdiscipline", "discipline_id", "sort_number", "is_active",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(SubDiscipline, SOPSubdisciplineAdmin)