from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import (
                    CharField,
                    EmailField,
                    BooleanField
                    )

from core.models import Model
from .managers import UserManager


class Account(Model, AbstractBaseUser, PermissionsMixin):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255, null=True)
    email = EmailField(max_length=255, unique=True)
    password = CharField(max_length=255)
    phone = CharField(max_length=255, null=True)

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


