from django.contrib import admin

from projects.models import *
		
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active", "sort_number",)
    search_fields = ["the_name",]
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(ProjectStatus, ProjectStatusAdmin)

class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    search_fields = ["the_name",]
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(ProjectType, ProjectTypeAdmin)

class QappStatusAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    search_fields = ["the_name", ]
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(QappStatus, QappStatusAdmin)

class QaCategoryAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    search_fields = ["the_name",]
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(QaCategory, QaCategoryAdmin)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    search_fields = ["the_name",]
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(Program, ProgramAdmin)

class NRMRLQAPPRequirementAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active", "sort_number",)
    search_fields = ["the_name", "is_active",]
    list_filter = ("the_name", "is_active",)
    list_per_page = 25

admin.site.register(NRMRLQAPPRequirement, NRMRLQAPPRequirementAdmin)

class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    search_fields = ["the_name", ]
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(VehicleType, VehicleTypeAdmin)

# Not in use.
# class ProjectCategoryAdmin(admin.ModelAdmin):
#     list_display = ("the_name", "is_active",)
#     search_fields = ["the_name", "is_active",]
#     list_filter = ("the_name", "is_active",)
#     list_per_page = 25
#
# admin.site.register(ProjectCategory, ProjectCategoryAdmin)

# Not sure people should edit this.
# class ProjectNumberAdmin(admin.ModelAdmin):
#     list_display = ("the_name", "start_serial_number", "this_serial_number", "next_serial_number",)
#     search_fields = ["the_name", "start_serial_number", "this_serial_number", "next_serial_number",]
#     list_filter = ("the_name", "start_serial_number", "this_serial_number", "next_serial_number",)
#     list_per_page = 25
#
# admin.site.register(ProjectNumber, ProjectNumberAdmin)

class ParticipatingOrganizationAdmin(admin.ModelAdmin):
    list_display = ("company", )
    search_fields = ["company", ]
    list_per_page = 25

admin.site.register(ParticipatingOrganization, ParticipatingOrganizationAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("qa_id", "title","project_status","restrict_qapp_files","restrict_ext_package_files",)
    search_fields = ["qa_id", "title",]
    list_filter = ("project_status", "project_type", "restrict_qapp_files","restrict_ext_package_files","qa_category","qapp_status")
    list_per_page = 25

admin.site.register(Project, ProjectAdmin)

class ProjectLogTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active",)
    search_fields = ["the_name",]
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(ProjectLogType, ProjectLogTypeAdmin)

class ReviewTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", )
    search_fields = ["the_name", ]
    list_per_page = 25

admin.site.register(ReviewType, ReviewTypeAdmin)

class ProjectLogAdmin(admin.ModelAdmin):
    list_display = ("qa_log_number", "title", "project_log_type",)
    search_fields = ["qa_log_number", "title",]
    list_filter = ("project_log_type", "review_type",)
    list_per_page = 25

admin.site.register(ProjectLog, ProjectLogAdmin)


class Project_update_historyAdmin(admin.ModelAdmin):
    list_display = ("modified", "user","comments")
    search_fields = ["project", "user",]
    list_filter = ("project",)
    list_per_page = 25

admin.site.register(Project_update_history, Project_update_historyAdmin)

class ProjectLog_update_historyAdmin(admin.ModelAdmin):
    list_display = ("modified", "project_log","user","comments")
    search_fields = ["project_log", "user",]
    list_filter = ("project_log",)
    list_per_page = 25

admin.site.register(ProjectLog_update_history, ProjectLog_update_historyAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active", "sort_number",)
    search_fields = ["the_name", "is_active",]
    list_filter = ("the_name", "is_active",)
    list_per_page = 25

admin.site.register(ProductCategory, ProductCategoryAdmin)