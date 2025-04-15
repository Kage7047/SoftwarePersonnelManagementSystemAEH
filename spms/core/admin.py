from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmployeeProfile, LeaveRequest, Task

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(EmployeeProfile)
admin.site.register(LeaveRequest)
admin.site.register(Task)

