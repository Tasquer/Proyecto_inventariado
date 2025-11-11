from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def rol_requerido(roles_permitidos=[]):
    """
    Un decorador para verificar el rol del usuario.
    Redirige al login si no está logueado, o muestra
    un error 403 (Permiso Denegado) si no tiene el rol.
    
    Uso:
    @rol_requerido(roles_permitidos=['ADMIN', 'GERENCIA'])
    def mi_vista_protegida(request):
        ...
    """
    def decorador(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                
                return redirect('usuarios:login') 
            
           
            if request.user.rol not in roles_permitidos:
                raise PermissionDenied("No tienes permiso para ver esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorador