from django.contrib import admin
from .models import InstructorProfile, StudentTaskStatus, Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'xp_reward','deadline']

class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']

class StudentTaskStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'task', 'completed']

admin.site.register(Task,TaskAdmin)
admin.site.register(InstructorProfile, InstructorProfileAdmin)
admin.site.register(StudentTaskStatus, StudentTaskStatusAdmin)
