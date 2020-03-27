from django.contrib import admin

from persons.models import *

# Not in use so commented out.
# class PersonStatusAdmin(admin.ModelAdmin):
#     list_display = ("the_name", )
#     search_fields = ("the_name", )
#     list_filter = ("the_name", )
#     list_per_page = 25
#
# admin.site.register(PersonStatus, PersonStatusAdmin)
#
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ("last_name", "first_name",)
#     search_fields = ("last_name", "first_name",)
#     list_filter = ("last_name", "first_name",)
#     list_per_page = 25
#
# admin.site.register(Person, PersonAdmin)
#
# class PersonEmergencyContactAdmin(admin.ModelAdmin):
#     list_display = ("last_name", "first_name",)
#     search_fields = ("last_name", "first_name",)
#     list_filter = ("last_name", "first_name",)
#     list_per_page = 25
#
# admin.site.register(PersonEmergencyContact, PersonEmergencyContactAdmin)