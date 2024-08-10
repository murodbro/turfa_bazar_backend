from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError(_("Email must be set!"))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):

        if not email:
            raise ValueError(_("Email must be set!"))
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

