# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
# ¡Importamos el modelo para poder usar los roles!
from .models import Usuario 

# ... (Aquí va tu función add_bootstrap_classes) ...
def add_bootstrap_classes(form):
    # ... (tu código de bootstrap)
    pass

# --- Formulario de Registro (CORREGIDO) ---

class RegistroForm(UserCreationForm):
    """
    Formulario de creación de usuarios. 
    ¡YA NO PREGUNTA EL ROL!
    """
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese una dirección de correo válida.")
    
    # !!! --- CAMBIO IMPORTANTE --- !!!
    # Hemos ELIMINADO el campo 'rol' de aquí. 
    # Ya no será visible en el formulario.

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # !!! --- CAMBIO IMPORTANTE --- !!!
        # Quitamos 'rol' de los campos que el usuario debe rellenar.
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_bootstrap_classes(self) # Aplicamos Bootstrap

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # !!! --- LÓGICA DE SEGURIDAD --- !!!
        # Asignamos el rol por defecto. 
        # Todo usuario que se registre será 'Personal Operativo'.
        user.rol = Usuario.Roles.OPERATIVO
        
        if commit:
            user.save()
        return user

# --- Formularios de Edición de Perfil ---
# (Estos quedan igual)

class UsuarioInfoForm(forms.ModelForm):
    # ... (sin cambios)
    pass

class FotoForm(forms.ModelForm):
    # ... (sin cambios)
    pass