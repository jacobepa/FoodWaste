
from constants.models import *

from branches.models import *
from divisions.models import *
from labs.models import *

from django.urls import reverse

def get_person_storage_path(instance, filename):
	return '%s/person/%s' %(instance.user.username, filename)

class PersonStatus(models.Model):
	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
	modified_on = models.DateField(auto_now=True, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	created_by = models.CharField(blank=True, null=True, max_length=255)
	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	
	the_name = models.CharField(max_length=255)
	
	def __str__(self):
		return self.the_name or ''
		
class Person(models.Model):
	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
	modified_on = models.DateField(auto_now=True, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	created_by = models.CharField(blank=True, null=True, max_length=255)
	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
	is_reviewer = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
	
	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
		
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	person_status = models.ForeignKey(PersonStatus, on_delete=models.CASCADE, null=True, blank=True)
	lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True, blank=True)
	division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	
	badge_number = models.CharField(null=True, blank=True, max_length=25)
	other_number = models.CharField(null=True, blank=True, max_length=25)
	
	weblink = models.CharField(blank=True, null=True, max_length=255)
	ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)
	
	title = models.CharField(blank=True, null=True, max_length=255)
	salutation = models.CharField(blank=True, null=True, max_length=255)
	
	date_started = models.DateField(null=True, blank=True)
	date_ended = models.DateField(null=True, blank=True)
	
	class Meta:
		ordering = ['ordering', 'last_name', 'first_name']
	
	def __str__(self):
		return self.last_name + ', ' + self.first_name or ''
		
		
class PersonEmergencyContact(models.Model):
	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
	modified_on = models.DateField(auto_now=True, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	created_by = models.CharField(blank=True, null=True, max_length=255)
	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)

	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)

	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)

	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)

	phone_number = models.CharField(null=True, blank=True, max_length=25)
	email_address = models.CharField(null=True, blank=True, max_length=25)

	weblink = models.CharField(blank=True, null=True, max_length=255)
	ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)

	title = models.CharField(blank=True, null=True, max_length=255)
	relationship = models.CharField(blank=True, null=True, max_length=255)

	class Meta:
		ordering = ['ordering', 'last_name', 'first_name']

	def __str__(self):
		return self.last_name + ', ' + self.first_name or ''
#
# class PersonAttachment(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# 	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
#
# class AddressType(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#
# 	the_name = models.CharField(max_length=255)
#
# 	def __str__(self):
# 		return self.the_name
#
# class PersonAddress(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# 	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
#
# 	address_type = models.ForeignKey(AddressType, on_delete=models.CASCADE, null=True, blank=True)
#
# 	street_address_01 = models.CharField(blank=True, null=True, max_length=255)
# 	street_address_02 = models.CharField(blank=True, null=True, max_length=255)
# 	city = models.CharField(blank=True, null=True, max_length=255)
# 	state = models.CharField(blank=True, null=True, max_length=255)
# 	zipcode = models.CharField(blank=True, null=True, max_length=255)
# 	mail_station = models.CharField(blank=True, null=True, max_length=255)
# 	building = models.CharField(blank=True, null=True, max_length=255)
# 	private_mailbox_designator = models.CharField(blank=True, null=True, max_length=255)
# 	special_instruction = models.CharField(blank=True, null=True, max_length=255)
# 	region = models.CharField(blank=True, null=True, max_length=255)
# 	title = models.CharField(blank=True, null=True, max_length=255)
# 	serving = models.CharField(blank=True, null=True, max_length=255)
# 	office = models.CharField(blank=True, null=True, max_length=255)
#
# 	def __str__(self):
# 		return self.street_address_01
#
#
# class EmailType(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#
# 	the_name = models.CharField(max_length=255)
#
# 	def __str__(self):
# 		return self.the_name
#
# class PersonEmail(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# 	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
#
# 	email_type = models.ForeignKey(EmailType, on_delete=models.CASCADE, null=True, blank=True)
#
# 	email_address = models.CharField(blank=True, null=True, max_length=255)
# 	instruction = models.CharField(blank=True, null=True, max_length=255)
#
# 	def __str__(self):
# 		return self.email_address
#
# class PhoneType(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#
# 	the_name = models.CharField(max_length=255)
#
# 	def __str__(self):
# 		return self.the_name
#
# class PersonPhone(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# 	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
#
# 	phone_type = models.ForeignKey(PhoneType, on_delete=models.CASCADE, null=True, blank=True)
#
# 	phone_number = models.CharField(blank=True, null=True, max_length=255)
# 	extension = models.CharField(blank=True, null=True, max_length=255)
# 	instruction = models.CharField(blank=True, null=True, max_length=255)
#
# 	def __str__(self):
# 		return self.email_address
#
# class PersonDivisionBranch(models.Model):
# 	created_on = models.DateField(auto_now_add=True, null=True, blank=True)
# 	modified_on = models.DateField(auto_now=True, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# 	modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# 	created_by = models.CharField(blank=True, null=True, max_length=255)
# 	last_modified_by = models.CharField(blank=True, null=True, max_length=255)
# 	share = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
#
# 	attachment = models.FileField(null=True, blank=True, upload_to=get_person_storage_path)
#
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# 	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
# 	division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
# 	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
#
# 	badge_number = models.CharField(null=True, blank=True, max_length=25)
# 	other_number = models.CharField(null=True, blank=True, max_length=25)
#
# 	weblink = models.CharField(blank=True, null=True, max_length=255)
# 	ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)
#
# 	title = models.CharField(blank=True, null=True, max_length=255)
# 	salutation = models.CharField(blank=True, null=True, max_length=255)
#
# 	date_started = models.DateField(null=True, blank=True)
# 	date_ended = models.DateField(null=True, blank=True)
#
# 	def __str__(self):
# 		return self.person.last_name
#
