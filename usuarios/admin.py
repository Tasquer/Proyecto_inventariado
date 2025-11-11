from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    

    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol', 'foto')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol', 'foto')}),
    )
    

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'rol']
    
    list_filter = UserAdmin.list_filter + ('rol',)