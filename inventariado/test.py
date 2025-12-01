import pytest
from miapp.models import TuModelo

# MARKER: Esto es OBLIGATORIO si tu test toca la base de datos
@pytest.mark.django_db
def test_crear_modelo():
    nombre = "Prueba Pytest"
    
    obj = TuModelo.objects.create(nombre=nombre)
    
    assert obj.nombre == "Prueba Pytest"
    assert obj.pk is not None