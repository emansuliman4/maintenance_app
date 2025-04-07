from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Custom User Manager
class Manager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, username=username or email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password=password, **extra_fields)

    def create_manager(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'manager')
        return self.create_user(email, password, **extra_fields)

    def create_employee(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'employee')
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
