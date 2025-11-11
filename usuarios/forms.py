# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
# ¡Importamos el modelo para poder usar los roles!
from .models import Usuario 

# --- Función Helper para añadir clases de Bootstrap ---
def add_bootstrap_classes(form):
    """
    Añade la clase 'form-control' de Bootstrap a todos los campos
    de un formulario.
    """
    for field_name, field in form.fields.items():
        widget = field.widget
        existing_classes = widget.attrs.get('class', '')
        
        if 'form-control' not in existing_classes:
            if not isinstance(widget, (forms.CheckboxInput, forms.FileInput)):
                widget.attrs['class'] = (existing_classes + ' form-control').strip()
            elif isinstance(widget, forms.FileInput):
                widget.attrs['class'] = (existing_classes + ' form-control').strip()
            else:
                widget.attrs['class'] = (existing_classes + ' form-check-input').strip()

# --- Formulario de Registro (CORREGIDO) ---

class RegistroForm(UserCreationForm):
    """
    Formulario de creación de usuarios. 
    ¡YA NO PREGUNTA EL ROL!
    """
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese una dirección de correo válida.")
    
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_bootstrap_classes(self) # Aplicamos Bootstrap

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.rol = Usuario.Roles.OPERATIVO
        
        if commit:
            user.save()
        return user

# --- Formularios de Edición de Perfil ---
# ¡AQUÍ ESTÁ LA CORRECCIÓN!

class UsuarioInfoForm(forms.ModelForm):
    """
    Formulario para editar la información básica del usuario.
    """
    class Meta:
        model = Usuario  # <-- ESTO ES LO QUE FALTABA
        fields = ['username', 'email', 'first_name', 'last_name'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_bootstrap_classes(self) # Aplicamos Bootstrap

class FotoForm(forms.ModelForm):
    """
    Formulario dedicado solo a cambiar la foto de perfil.
    """
    class Meta:
        model = Usuario  # <-- ESTO ES LO QUE FALTABA
        fields = ['foto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_bootstrap_classes(self) # Aplicamos Bootstrap