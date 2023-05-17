from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to="images/profile", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name"]

    objects = AccountManager()

    def __str__(self):
        return self.username
