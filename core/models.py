from statistics import mode
from django.db import models
from django.contrib.auth import models as auth_models
from core import managers as core_managers
from django.core.validators import RegexValidator
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class User(auth_models.AbstractUser):
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []
    EMAIL_FIELD = "mobile"
    email=None
    username = models.CharField(max_length=30, null=True, blank=True)
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17,db_index=True, unique=True)    
    is_mobile_verified = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = "users"
        verbose_name_plural = "users"

    objects = core_managers.UserManager()
    
    def save(self, *args, **kwargs):
        if 'pbkdf' not in self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    
    def get_details(self):
        return {
            "username":self.username,
            "emails":[obj.get_details() for obj in self.user_emails.filter(is_deleted=False)],
            "mobile":self.mobile
        }
        
class UserEmail(BaseModel):
    user = models.ForeignKey("core.User", related_name="user_emails", on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True, null=True, db_index=True)
    is_primary = models.BooleanField(default=False)


    def get_details(self):
        return {
            "email":self.email,
            "is_primary":self.is_primary
        }