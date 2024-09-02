from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    "Custom user model manager where email is the unique identifiers for authentication instead of usernames."

    def _create_user(self, email, password, **extra_fields):
        "Create and save a User with the given email and password."

        if not email:
            raise ValueError(_("The Email must be set"))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password=password, **extra_fields)


class UserRoleType(Enum):
    USER = "user"
    ADMIN = "admin"


class User(AbstractBaseUser, PermissionsMixin):
    __REPR__ = ("id", "name", "email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    age = models.IntegerField(null=True, blank=True)
    role = models.CharField(
        max_length=32,
        choices=[(role.name, role.value) for role in UserRoleType],
        default=UserRoleType.USER.value,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.name} - {self.email}"
