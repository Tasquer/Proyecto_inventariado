# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    
    # --- Roles del Proyecto ---
    # [cite_start]Basado en tu EV2 [cite: 61, 323, 324, 326] y tu rúbrica
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'       # Acceso total
        OPERATIVO = 'OPERATIVO', 'Personal Operativo' # CRUD de inventario
        GERENCIA = 'GERENCIA', 'Gerencia'         # Ver reportes y análisis

    # --- Campos ---
    # El campo 'rol' está ahora *dentro* del modelo de Usuario
    rol = models.CharField(
        max_length=50, 
        choices=Roles.choices, 
        default=Roles.OPERATIVO,  # Un default seguro, puedes cambiarlo
        help_text='Rol del usuario en el sistema'
    )
    
    # Foto de perfil (opcional, como tenías en tu 'Perfil')
    foto = models.ImageField(
        upload_to='fotos_perfil/', 
        blank=True, 
        null=True,
        help_text='Foto de perfil del usuario'
    )

    def __str__(self):
        # Mostramos el username y su rol
        return f"{self.username} ({self.get_rol_display()})"