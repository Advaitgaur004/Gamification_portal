from django.contrib import admin
from .models import InstructorProfile, StudentTaskStatus, Task,Extra_TA

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'xp_reward','deadline']

class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']

class StudentTaskStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'task', 'completed']

class Extra_TAAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'faculty']

admin.site.register(Task,TaskAdmin)
admin.site.register(InstructorProfile, InstructorProfileAdmin)
admin.site.register(StudentTaskStatus, StudentTaskStatusAdmin)
admin.site.register(Extra_TA, Extra_TAAdmin)
