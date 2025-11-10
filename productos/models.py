from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    cantidad = models.IntegerField(default=1)
    
    fecha_caducidad = models.DateField(
        null=True, 
        blank=True
    )
    
    descripcion = models.TextField(
        blank=True, 
        null=True
    )
    
    fecha_agregado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"