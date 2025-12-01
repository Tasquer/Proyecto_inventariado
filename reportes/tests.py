import pytest
import json
from django.urls import reverse
from productos.models import Producto, Categoria

# 1. Fixture para crear usuario (necesario por el @login_required)
@pytest.fixture
def usuario(django_user_model):
    return django_user_model.objects.create_user(
        username='report_user', 
        password='password123'
    )

# 2. Prueba de Seguridad: Acceso denegado a anónimos
@pytest.mark.django_db
def test_vista_reporte_requiere_login(client):
    """Verifica que si no estás logueado, te redirige al login"""
    url = reverse('reportes:vista_principal')  # Definido en tu urls.py
    resp = client.get(url)
    assert resp.status_code == 302  # Redirección
    assert '/login' in resp.url or '/accounts/login' in resp.url

# 3. Prueba de Lógica: Verificar que cuenta bien los productos
@pytest.mark.django_db
def test_reporte_calcula_totales_correctos(client, usuario):
    """
    Crea productos en diferentes categorías y verifica que 
    la vista retorne el JSON con los conteos correctos.
    """
    # A. PREPARAR (Arrange)
    # Creamos 2 categorías
    cat_tech = Categoria.objects.create(nombre="Tecnología")
    cat_hogar = Categoria.objects.create(nombre="Hogar")

    # Creamos 3 productos: 2 de Tecnología, 1 de Hogar
    # (Ajusta los campos según tu modelo Producto si tienes más obligatorios)
    Producto.objects.create(nombre="Mouse", categoria=cat_tech, cantidad=10, )
    Producto.objects.create(nombre="Teclado", categoria=cat_tech, cantidad=5, )
    Producto.objects.create(nombre="Silla", categoria=cat_hogar, cantidad=1, )

    # B. ACTUAR (Act)
    client.force_login(usuario)
    url = reverse('reportes:vista_principal')
    resp = client.get(url)

    # C. VERIFICAR (Assert)
    assert resp.status_code == 200
    
    # Verificar que el contexto tiene las variables del gráfico
    assert 'chart_labels' in resp.context
    assert 'chart_datasets' in resp.context

    # Tu vista devuelve strings JSON (json.dumps), así que los convertimos a dicts/listas
    labels = json.loads(resp.context['chart_labels'])
    datasets = json.loads(resp.context['chart_datasets'])

    # Verificaciones específicas de datos:
    # 1. ¿Están las categorías en las etiquetas?
    assert "Tecnología" in labels
    assert "Hogar" in labels

    # 2. Tu vista ordena por '-total' (descendente), así que Tecnología (2 productos) va primero
    assert labels[0] == "Tecnología"
    
    # 3. Verificar los números en el dataset
    # data_counts está dentro de datasets[0]['data']
    datos = datasets[0]['data']
    assert datos[0] == 2  # 2 productos de tecnología
    assert datos[1] == 1  # 1 producto de hogar