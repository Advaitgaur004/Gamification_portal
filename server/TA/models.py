from django.db import models
from django.contrib.auth.models import User, AbstractUser,Group, Permission
from Student.models import StudentProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .service import get_enrolled_students
import uuid

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    xp_reward = models.IntegerField()
    deadline = models.DateTimeField(null=True, blank=True)
    sheet_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Task)
def assign_tasks_to_students(sender, instance, created, **kwargs):
    if created:
        enrolled_students = get_enrolled_students(sheet_name="Testing_GP", worksheet_name="Sheet1")
        for student_rollno in enrolled_students:
            try:
                student = StudentProfile.objects.get(Rollno=student_rollno)
                if student:
                    student.tasks.add(instance)
                    student.save()
            except StudentProfile.DoesNotExist:
                pass
        
class InstructorProfile(models.Model):
    username = models.CharField(max_length=255, unique=True,null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default='cb8f6a9d787f59ca')
    refreshtoken = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.username

class StudentTaskStatus(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    earned_xp = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.user.username} - {self.task.title}"


class Extra_TA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.OneToOneField(InstructorProfile, on_delete=models.CASCADE)