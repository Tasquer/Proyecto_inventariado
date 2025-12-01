import pytest
from django.urls import reverse
from .models import Producto, Categoria

# Este fixture crea un usuario temporal para usar en las pruebas
@pytest.fixture
def usuario_prueba(django_user_model):
    return django_user_model.objects.create_user(
        username='testuser', 
        password='password123'
    )

# Este fixture crea una categoría, ya que Producto tiene una ForeignKey a ella
@pytest.fixture
def categoria_prueba():
    return Categoria.objects.create(nombre="Electrónica")

@pytest.mark.django_db
def test_crear_producto_exitoso(client, usuario_prueba, categoria_prueba):
    """
    Prueba que un usuario logueado puede crear un producto correctamente.
    """
    # 1. Iniciar sesión con el usuario de prueba
    client.force_login(usuario_prueba)

    # 2. Definir los datos del formulario (basado en tu models.py)
    datos_producto = {
        'nombre': 'Laptop Gamer',
        'categoria': categoria_prueba.id,  # Pasamos el ID de la categoría
        'cantidad': 10,
        'fecha_caducidad': '2025-12-31',
        'descripcion': 'Una laptop muy potente'
    }

    # 3. Hacer la petición POST a la URL de creación
    # Asumo que tu URL se llama 'productos:crear', ajusta esto según tu urls.py
    # Si no sabes el nombre, puedes poner la ruta directa ej: '/productos/crear/'
    url = reverse('productos:crear') 
    respuesta = client.post(url, data=datos_producto)

    # 4. Verificar Assertions (Afirmaciones)
    
    # A) Verificar que redirige al dashboard (código 302) como indica tu success_url
    assert respuesta.status_code == 302
    assert respuesta.url == reverse('dashboard')

    # B) Verificar que el producto se guardó en la base de datos
    assert Producto.objects.count() == 1
    
    # C) Verificar que los datos son correctos
    producto_creado = Producto.objects.first()
    assert producto_creado.nombre == 'Laptop Gamer'
    assert producto_creado.categoria == categoria_prueba
    assert producto_creado.cantidad == 10