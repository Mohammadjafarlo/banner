from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import random, os, string

def random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def rename_random_file(instance, filename):
    """Rename file to a random string."""
    ext = filename.split('.')[-1]
    new_filename = f"{random_string()}.{ext}"
    return os.path.join('profile_images/', new_filename)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """Create and return a regular user."""
        if not username:
            raise ValueError(_('The Username field must be set'))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Create and return a superuser with superuser permissions."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=30, unique=True)
    # Remove password field as it is handled by AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=rename_random_file, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']
    
    def __str__(self):
        return self.username
