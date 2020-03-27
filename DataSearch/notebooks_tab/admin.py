from django.contrib import admin

# Register your models here.
from notebooks_tab.models import *

class NotebookAdmin(admin.ModelAdmin):
    list_display = ("nb_number", "title",'status', "nb_type")
    search_fields = ["nb_number", "title",]
    list_filter = ('status_id',"nb_type")
    list_per_page = 25

admin.site.register(NotebooksTab, NotebookAdmin)

class NotebookTypeAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active", "sort_number",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(NotebooksTab_Type, NotebookTypeAdmin)

class NotebookNBStatusAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active", "sort_number",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(NotebooksTab_NotebookStatus, NotebookNBStatusAdmin)

class NotebookStatusAdmin(admin.ModelAdmin):
    list_display = ("the_name", "is_active", "sort_number",)
    list_filter = ("is_active",)
    list_per_page = 25

admin.site.register(NotebooksTab_Status, NotebookStatusAdmin)

class NotebookReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "nbtab", "user", "reviewer", 'status')
    search_fields = ["id", "nbtab_id__nb_number",]
    list_filter = ('status_id',)
    list_per_page = 25

admin.site.register(NotebooksTab_Reviews, NotebookReviewAdmin)

