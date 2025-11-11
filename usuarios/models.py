from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    
    class Roles(models.TextChoices):
        OPERATIVO = 'OPERATIVO', 'Personal Operativo' 
        GERENCIA = 'GERENCIA', 'Gerencia'        


    rol = models.CharField(
        max_length=50, 
        choices=Roles.choices, 
        default=Roles.OPERATIVO,  
        help_text='Rol del usuario en el sistema'
    )
    
  
    foto = models.ImageField(
        upload_to='fotos_perfil/', 
        blank=True, 
        null=True,
        help_text='Foto de perfil del usuario'
    )

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"