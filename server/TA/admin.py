from django.contrib import admin
from .models import InstructorProfile, StudentTaskStatus, Task

admin.site.register(Task)
admin.site.register(InstructorProfile)
admin.site.register(StudentTaskStatus)
