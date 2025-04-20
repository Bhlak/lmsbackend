from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    fieldsets=(
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
         
    )
    
    list_display = ["email", "id"]

    search_fields = ("email",)
    ordering = ("id", )