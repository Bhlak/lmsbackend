from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import AppUser, Student


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    fieldsets=(
        (None, {'fields': ('email', 'firstname', 'lastname', 'password', 'loaned')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
         
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff'),
        }),
    )
    
    list_display = ["email", "firstname", "lastname", "id", "loaned", "banned"]

    search_fields = ("email",)
    ordering = ("id", )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student
    fieldsets=(
        (None, {'fields': ('matric_no', 'user')}),
    )

    list_display = ["user", "matric_no"]

    search_fields = ("matric_no",)
