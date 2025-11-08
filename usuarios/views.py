# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Importamos TODOS los formularios que creamos
from .forms import RegistroForm, UsuarioInfoForm, FotoForm

# --- Vistas de Autenticación ---

def registro_view(request):
    """
    Controla el registro de nuevos usuarios.
    """
    # Si el usuario ya está logueado, lo redirigimos
    if request.user.is_authenticated:
        return redirect('usuarios:perfil') # O a un 'home'
    
    if request.method == 'POST':
        # El usuario envió el formulario
        form = RegistroForm(request.POST)
        if form.is_valid():
            # El formulario es válido, guardamos al usuario
            form.save()
            
            # Mostramos un mensaje de éxito
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada exitosamente para {username}! Ya puedes iniciar sesión.')
            
            # Lo redirigimos al login
            return redirect('usuarios:login')
    else:
        # El usuario está pidiendo la página (GET)
        form = RegistroForm()
        
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    """
    Controla el inicio de sesión.
    """
    if request.user.is_authenticated:
        return redirect('usuarios:perfil') # O a un 'home'
    
    if request.method == 'POST':
        # Usamos el AuthenticationForm nativo de Django
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Autenticamos al usuario
            usuario = authenticate(username=username, password=password)
            
            if usuario is not None:
                # Si la autenticación es exitosa, lo logueamos
                login(request, usuario)
                messages.info(request, f'¡Bienvenido de vuelta, {username}!')
                
                # TODO: Cuando tengamos la app de 'productos', 
                # cambiaremos esto a la lista de productos.
                return redirect('usuarios:perfil') 
            else:
                # Si no, mostramos un error
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    # Si es GET, mostramos el formulario de login
    form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


@login_required # Este decorador protege la vista
def logout_view(request):
    """
    Cierra la sesión del usuario.
    """
    username = request.user.username
    logout(request)
    messages.info(request, f'Has cerrado sesión. ¡Hasta pronto, {username}!')
    return redirect('usuarios:login')


# --- Vistas de Perfil ---

@login_required # Protegemos también el perfil
def perfil_view(request):
    """
    Muestra la página de perfil del usuario logueado.
    """
    # No necesitamos pasar 'user' al template, Django lo hace
    # automáticamente con 'request.user'.
    # ¡Y no necesitamos 'perfil' porque nuestro modelo ya tiene el rol!
    return render(request, 'usuarios/perfil.html')


# --- ¡NUEVA VISTA AÑADIDA! ---

@login_required
def editar_perfil_view(request):
    """
    Controla la edición de la información del perfil y la foto.
    """
    if request.method == 'POST':
        # El usuario está guardando cambios
        # Pasamos 'instance=request.user' para decirle a los formularios
        # qué usuario estamos editando.
        user_form = UsuarioInfoForm(request.POST, instance=request.user)
        
        # 'request.FILES' es crucial para manejar la subida de la foto
        foto_form = FotoForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid() and foto_form.is_valid():
            # Si ambos formularios son válidos, los guardamos
            user_form.save()
            foto_form.save()
            
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('usuarios:perfil')
        else:
            # Si hay un error, los mensajes de error se mostrarán
            # en los formularios automáticamente.
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    else:
        # El usuario está pidiendo la página (GET)
        # Le mostramos los formularios pre-rellenados con su info actual
        user_form = UsuarioInfoForm(instance=request.user)
        foto_form = FotoForm(instance=request.user)

    # Preparamos el contexto para pasar ambos formularios al template
    context = {
        'user_form': user_form,
        'foto_form': foto_form
    }
    return render(request, 'usuarios/editar_perfil.html', context)