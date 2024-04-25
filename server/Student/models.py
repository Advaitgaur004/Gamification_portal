from django.db import models
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Rollno = models.CharField(max_length=255)
    email = models.EmailField()
    badge = models.ManyToManyField(to='Badge', blank=True)
    tasks = models.ManyToManyField(to='TA.Task', blank=True)
    total_xp = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
