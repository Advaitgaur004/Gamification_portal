from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User 
Badge_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
    ('Expert', 'Expert')
)


class Badge(models.Model):
    name = models.CharField(max_length=255, choices=Badge_CHOICES, default='Beginner')
    description = models.TextField()
    xp_required = models.IntegerField()

class StudentProfile(models.Model):
    username = models.CharField(max_length=255, unique=True,null=True)
    Rollno = models.CharField(max_length=255)
    email = models.EmailField(unique=True,null=False)
    badge = models.ManyToManyField(to='Badge', blank=True)
    tasks = models.ManyToManyField(to='TA.Task', blank=True)
    password = models.CharField(max_length=128, default='cb8f6a9d787f59ca')
    refreshtoken = models.CharField(max_length=255,null=True,blank=True)
    total_xp = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     email = self.email.split('@')[-1]
    #     if email != 'iitj.ac.in':
    #         raise ValueError('Student Not from IIT jodhpur')
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Extra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)