from django.contrib import admin

# Import the model
from profiles_api import models

# Register your models here.
# This line registers the UserProfile model
admin.site.register(models.UserProfile)
