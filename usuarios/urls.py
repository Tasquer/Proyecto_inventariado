# usuarios/urls.py
from django.urls import path
from . import views  # Importamos las vistas (que crearemos después)

# Esto es crucial para que {% url 'usuarios:login' %} funcione
app_name = 'usuarios'

urlpatterns = [
    # Ruta para el registro
    # http://127.0.0.1:8000/usuarios/registro/
    path('registro/', views.registro_view, name='registro'),

    # Ruta para el login
    # http://127.0.0.1:8000/usuarios/login/
    path('login/', views.login_view, name='login'),

    # Ruta para el logout
    # http://127.0.0.1:8000/usuarios/logout/
    path('logout/', views.logout_view, name='logout'),

    # Ruta para ver el perfil
    # http://127.0.0.1:8000/usuarios/perfil/
    path('perfil/', views.perfil_view, name='perfil'),

    # Ruta para editar el perfil
    # http://127.0.0.1:8000/usuarios/editar_perfil/
    path('editar_perfil/', views.editar_perfil_view, name='editar_perfil'),
]