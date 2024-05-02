from django.contrib import admin
from .models import StudentProfile, Badge, Extra

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'email', 'Rollno', 'total_xp']

class BadgeAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'xp_required']

admin.site.register(Badge, BadgeAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Extra)