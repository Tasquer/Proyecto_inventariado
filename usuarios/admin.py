# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Registramos el modelo Usuario personalizado
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    
    # Añadimos 'rol' y 'foto' a los formularios del admin
    # para que sean visibles y editables.
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol', 'foto')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol', 'foto')}),
    )
    
    # Añadimos 'rol' a la lista que se ve en el admin
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'rol']
    
    # Hacemos 'rol' filtrable
    list_filter = UserAdmin.list_filter + ('rol',)