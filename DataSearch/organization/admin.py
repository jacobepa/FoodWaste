from django.contrib import admin

from organization.models import *

class OfficeAdmin(admin.ModelAdmin):
    list_display = ("office", "id", "abbreviation",)
    search_fields = ["office", "abbreviation",]
    list_filter = ("office", "abbreviation",)
    list_per_page = 25

admin.site.register(Office, OfficeAdmin)

class LabAdmin(admin.ModelAdmin):
    list_display = ("lab", "id", "abbreviation", "designation_code", "office_id",)
    search_fields = ["lab", "abbreviation", "designation_code",]
    list_filter = ("office_id",)
    list_per_page = 25

admin.site.register(Lab, LabAdmin)

class DivisionAdmin(admin.ModelAdmin):
    list_display = ("division", "id", "abbreviation", "office_id", "lab_id", "is_active",)
    search_fields = ["division", "abbreviation",]
    list_filter = ("office_id", "lab_id", "is_active",)
    list_per_page = 25

admin.site.register(Division, DivisionAdmin)

class BranchAdmin(admin.ModelAdmin):
    list_display = ("branch", "id", "abbreviation", "office_id", "lab_id", "division_id", "is_active",)
    search_fields = ["branch", "abbreviation",]
    list_filter = ("office_id", "lab_id", "division_id", "is_active",)
    list_per_page = 25

admin.site.register(Branch, BranchAdmin)