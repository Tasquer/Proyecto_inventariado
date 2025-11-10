from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    # CRUD de Productos
    path('', views.ProductoListView.as_view(), name='lista'),
    path('agregar/', views.ProductoCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='eliminar'),
    
    # Categorías
    path('categorias/agregar/', views.CategoriaCreateView.as_view(), name='categoria_agregar'),
]