from django.contrib.auth import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('users must have a phone number')
        user_obj = self.model(
            mobile=mobile, **extra_fields
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password=None, **extra_fields):
        
        """Create and save a SuperUser with the given mobile and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, password, **extra_fields)
    