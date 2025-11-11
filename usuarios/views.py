from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


from .forms import RegistroForm, UsuarioInfoForm, FotoForm


def registro_view(request):
    """
    Controla el registro de nuevos usuarios.
    """
    
    if request.user.is_authenticated:
        return redirect('usuarios:perfil')
    
    if request.method == 'POST':
     
        form = RegistroForm(request.POST)
        if form.is_valid():
            
            form.save()
            
           
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada exitosamente para {username}! Ya puedes iniciar sesión.')
            
           
            return redirect('usuarios:login')
    else:
        
        form = RegistroForm()
        
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    """
    Controla el inicio de sesión.
    """
    if request.user.is_authenticated:
        return redirect('usuarios:perfil') 
    
    if request.method == 'POST':
       
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
       
            usuario = authenticate(username=username, password=password)
            
            if usuario is not None:
                
                login(request, usuario)
                messages.info(request, f'¡Bienvenido de vuelta, {username}!')
                
                return redirect('usuarios:perfil') 
            else:
              
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    

    form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Cierra la sesión del usuario.
    """
    username = request.user.username
    logout(request)
    messages.info(request, f'Has cerrado sesión.')
    return redirect('usuarios:login')




@login_required 
def perfil_view(request):
    """
    Muestra la página de perfil del usuario logueado.
    """
    return render(request, 'usuarios/perfil.html')


@login_required
def editar_perfil_view(request):
    """
    Controla la edición de la información del perfil y la foto.
    """
    if request.method == 'POST':

        user_form = UsuarioInfoForm(request.POST, instance=request.user)
        
        foto_form = FotoForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid() and foto_form.is_valid():
            user_form.save()
            foto_form.save()
            
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('usuarios:perfil')
        else:

            messages.error(request, 'Por favor corrige los errores en el formulario.')

    else:

        user_form = UsuarioInfoForm(instance=request.user)
        foto_form = FotoForm(instance=request.user)

    context = {
        'user_form': user_form,
        'foto_form': foto_form
    }
    return render(request, 'usuarios/editar_perfil.html', context)