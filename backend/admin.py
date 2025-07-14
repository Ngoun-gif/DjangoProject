from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Department ,    UserProfile , Subject


admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Subject)
