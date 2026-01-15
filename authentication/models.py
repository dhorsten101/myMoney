from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
	"""
	Custom user manager for email-based authentication.
	Provides get_by_natural_key (via BaseUserManager) which Django auth expects.
	"""

	use_in_migrations = True

	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError("The Email field must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		if password:
			user.set_password(password)
		else:
			user.set_unusable_password()
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		extra_fields.setdefault("is_active", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")
		return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	
	USERNAME_FIELD = "email"

	objects = UserManager()

	EMAIL_FIELD = "email"
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email
