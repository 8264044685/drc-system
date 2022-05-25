from django.contrib import admin
from core import models as core_models
# Register your models here.
admin.site.register(core_models.User)
admin.site.register(core_models.UserEmail)