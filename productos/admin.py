from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'cantidad', 'fecha_caducidad', 'fecha_agregado')
    list_filter = ('categoria', 'fecha_caducidad')
    search_fields = ('nombre', 'descripcion')
    date_hierarchy = 'fecha_agregado'