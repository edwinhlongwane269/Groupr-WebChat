from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django_countries.fields import CountryField
from g_auth.choices import ROLES

class G_AUTHUSER_MANAGER(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, date_of_birth, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
       
        if not role:
            raise ValueError('Users must have a role')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, date_of_birth, role, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class G_AUTH_USER_MODEL(AbstractBaseUser):
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    country = CountryField(blank_label="(select country)")
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    role = models.CharField(max_length=100, blank=True, null=True, choices=ROLES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = G_AUTHUSER_MANAGER()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth', 'role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin