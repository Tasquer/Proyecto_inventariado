from django import forms
from .models import Producto, Categoria


class ProductoForm(forms.ModelForm):
    """
    Formulario para crear o editar un Producto.
    """
    class Meta:
        model = Producto
        
        fields = [
            'nombre', 
            'categoria', 
            'cantidad', 
            'fecha_caducidad', 
            'descripcion'
        ]
        
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. Leche Entera 1L'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control', 
                'value': 1,
                'min': 0
            }),
            'fecha_caducidad': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date' 
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Descripción o notas adicionales...'
            }),
        }
       
        labels = {
            'nombre': 'Nombre del Producto',
            'fecha_caducidad': 'Fecha de caducidad (Opcional)',
            'categoria': 'Categoría',
            'cantidad': 'Cantidad',
            'descripcion': 'Descripción (Opcional)',
        }

# --- Formulario de Categoría ---
# forms.py
from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control border-start-0 ps-0', # border-start-0 para fusionarse con el icono
                'placeholder': 'Ej. Electrónica, Bebidas...',
                'autofocus': True
            })
        }