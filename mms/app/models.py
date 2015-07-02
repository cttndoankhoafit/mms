"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
# Create your models here.

#region Member

class Member(models.Model):
	CONST_GENDERS = (
		(u'Nam', u'Nam'),
		(u'Nữ', u'Nữ')
	)

	identify = models.CharField(u'Mã số', max_length=20, primary_key=True)
	first_name = models.CharField(u'Tên', max_length=8)
	last_name = models.CharField(u'Họ', max_length=128)
	gender =  models.CharField(u'Giới tính', max_length=3, null=True, choices=CONST_GENDERS, default=0)
	date_of_birth = models.DateField(u'Ngày sinh', null=True, blank=True, default=None)
	place_of_birth = models.CharField(u'Nơi sinh', max_length=128, null=True, blank=True, default=None)
	folk = models.CharField(u'Dân tộc', max_length=32, null=True, blank=True, default=None)
	religion = models.CharField(u'Tôn giáo', max_length=32, null=True, blank=True, default=None)
	address = models.CharField(u'Địa chỉ thường trú', max_length=128, null=True, blank=True, default=None)
	ward = models.CharField(u'Xã/Phường/Thị trấn', max_length=128, null=True, blank=True, default=None)
	district = models.CharField(u'Quận/Huyện/Thành phố thuộc tỉnh', max_length=128, null=True, blank=True, default=None)
	province = models.CharField(u'Tỉnh/Thành phố', max_length=128, null=True, blank=True, default=None)
	temporary_address = models.CharField(u'Địa chỉ tạm trú', max_length=128, null=True, blank=True, default=None)
	home_phone = models.CharField(u'Điện thoại', max_length=32, null = True, blank=True, default=None)	
	mobile_phone = models.CharField(u'Điện thoại di động', max_length=32, null = True, blank=True, default=None)
	email = models.EmailField(u'Email', max_length=128, null = True, blank=True, default=None)

	# If the member is a student, add member's admission date
	admission_date = models.DateField(u'Ngày nhập học', null=True, blank=True, default=None)

	def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
		# If the user's account is not exist, create new account in User model.
		# Your code here
		
		return super(Member, self).save(force_insert, force_update, using, update_fields)

	def delete(self, using = None):
		# If any user is deleted, delete the user that related it
		# Your code here

		return super(Member, self).delete(using)

#endregion

#region User

class UserManager(BaseUserManager):
	def create_user(self, username="", email=None, password=None, **extra_fields):
		now = timezone.now()
		if not email:
			raise ValueError('The given email must be set')
		email = UserManager.normalize_email(email)
		username = username if username else email
		user = self.model(username=username, email=email,
						is_staff=False, is_active=True, is_superuser=False,
						last_login=now, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password, **extra_fields):
		u = self.create_user(username, email, password, **extra_fields)
		u.is_staff = True
		u.is_active = True
		u.is_superuser = True
		u.save(using=self._db)
		return u

class ActiveUser(models.Manager):
	def get_query_set(self):
		return super(ActiveUser, self).get_query_set().filter(is_active=True)

class User(AbstractBaseUser, PermissionsMixin):
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	username = models.CharField(max_length=40, unique=True, db_index=True)
	email = models.EmailField(max_length=254, unique=True)
	
	member = models.ForeignKey(Member, null=True, blank=True, default=None)

	is_staff = models.BooleanField('staff status', default=False,
		help_text='Designates whether the user can log into this admin '
				'site.')
	is_active = models.BooleanField('active', default=True,
		help_text='Designates whether this user should be treated as '
						'active. Unselect this instead of deleting accounts.')

	objects = UserManager()
	active_users = ActiveUser()

	def get_short_name(self):
		return self.username

#endregion

#region Organization

class OrganizationType(models.Model):
	name = models.CharField(u'Loại tổ chức', max_length=128)

class OrganizationPosition(models.Model):
	organization_type = models.ForeignKey(OrganizationType)
	name = models.CharField(u'Tên vị trí', max_length=128)

class Organization(models.Model):
	name = models.CharField(u'Tên tổ chức', max_length=128)
	organization_type = models.ForeignKey(OrganizationType)

class OrganizationManager(models.Model):
	organization_manager = models.ForeignKey(Organization, related_name='organization_manager')
	organization_managed =  models.ForeignKey(Organization, related_name='organization_managed')

	class Meta:
		unique_together = ('organization_manager', 'organization_managed')

class OrganizationUserManager(models.Model):
	user = models.ForeignKey(User)
	organization = models.ForeignKey(Organization)
	position = models.ForeignKey(OrganizationPosition)

	def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
		# User's position must be related organization's type (models: OrganizationType, OrganizationPosition)
		#Your code here
	
		return super(OrganizationUserManager, self).save(force_insert, force_update, using, update_fields)

	class Meta:
		unique_together = ('user', 'organization', 'position')

class OrganizationMember(models.Model):
	organization = models.ForeignKey(Organization)
	member = models.ForeignKey(Member)

	class Meta:
		unique_together = ('organization', 'member')

#endregion

#region Activity

class ActivityType(models.Model):
	name = models.CharField(u'Loại hoạt động', max_length=128)

class Activity(models.Model):
	name = models.CharField(u'Tên hoạt động', max_length=128)
	activity_type = models.ForeignKey(ActivityType)

class ActivityEvent(models.Model):
	activity = models.ForeignKey(Activity)	
	name = models.CharField(u'Tên sự kiện', max_length=128)
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

class ActivityOrganization(models.Model):
	activity = models.ForeignKey(Activity)
	organization = models.ForeignKey(Organization)

	class Meta:
		unique_together = ('activity', 'organization')

class ActivityEventMemberParticipation(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(ActivityEvent)
	published = models.BooleanField(default=False)

	class Meta:
		unique_together = ('member', 'event')

#endregion

