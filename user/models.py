from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.utils import timezone
import uuid

# Custom user manager
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        """Base method for creating users"""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # For users created without passwords
        
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a regular user"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'receptionist')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'manager')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        return self._create_user(email, password, **extra_fields)

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        MANAGER = 'manager', _('Manager')
        RECEPTIONIST = 'receptionist', _('Receptionist')
        TECHNICIAN = 'technician', _('Technician')

    # Basic fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('email address'), 
        unique=True,
        max_length=255,
        error_messages={'unique': _('A user with that email already exists.')},
    )
    first_name = models.CharField(
        _('first name'), 
        max_length=50, 
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        _('last name'), 
        max_length=50, 
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    
    # Status fields
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.')
    )
    
    # Additional fields
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.RECEPTIONIST,
        help_text=_('User role within the organization')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # Custom related names for groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    # Configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the full name, with a space between first and last names"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """Return the first name as short name"""
        return self.first_name or self.email.split('@')[0]

    # Role properties
    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    @property
    def is_receptionist(self):
        return self.role == self.Role.RECEPTIONIST

    @property
    def is_technician(self):
        return self.role == self.Role.TECHNICIAN

    def save(self, *args, **kwargs):
        """Custom save method to ensure email is always normalized"""
        self.email = self.__class__.objects.normalize_email(self.email)
        super().save(*args, **kwargs)