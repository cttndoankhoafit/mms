from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.

#region MEMBER
class Member(models.Model):
	pass

#endregion 

#region USER
class User(AbstractBaseUser, PermissionsMixin):
	pass

#endregion

