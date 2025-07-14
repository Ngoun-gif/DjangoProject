from django.db import models

# backend/models.py
from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.department_name
    

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


# Subject Model
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subject_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subject_updated_by')

    def __str__(self):
        return self.subject_name
    

import os
# teacher Model
class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teacher_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teacher_updated_by')


    def delete(self, *args, **kwargs):
        # Delete the image file when the product is deleted
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        # Delete the old image if a new one is uploaded
        if self.pk:  # Only for updates (not new creations)
            old_teacher = Teacher.objects.get(pk=self.pk)
            if old_teacher.photo and old_teacher.photo != self.photo:
                if os.path.isfile(old_teacher.photo.path):
                    os.remove(old_teacher.photo.path)
        super().save(*args, **kwargs)

