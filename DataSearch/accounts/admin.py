from django.contrib import admin

from accounts.models import *
		
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user", "permissions", "display_in_dropdowns")
    search_fields = ("user__username", "user__id", "user__first_name", "user__last_name")
    exclude = ('created_by', 'last_modified_by',)
    list_filter = ("permissions","display_in_dropdowns", "can_edit", "is_reviewer", "user_type", "can_create_users",)
    list_per_page = 25

admin.site.register(UserProfile, UserProfileAdmin)

# Not in use.
# class RequestSubjectAdmin(admin.ModelAdmin):
#     list_display = ("the_name", )
#     exclude = ('created_by', 'last_modified_by')
#     list_filter = ("the_name", )
#     list_per_page = 25
#
# admin.site.register(RequestSubject, RequestSubjectAdmin)
#
# class ContactRequestAdmin(admin.ModelAdmin):
#     list_display = ("request_subject", "the_name", "email_address" )
#     exclude = ('created_by', 'last_modified_by')
#     list_filter = ("request_subject","the_name", )
#     list_per_page = 25
#
# admin.site.register(ContactRequest, ContactRequestAdmin)