# reportes/views.py
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from productos.models import Producto, Categoria

# Lista de colores para el gráfico
CATEGORIA_COLORES = [
    'rgba(255, 99, 132, 0.7)',
    'rgba(54, 162, 235, 0.7)',
    'rgba(255, 206, 86, 0.7)',
    'rgba(75, 192, 192, 0.7)',
    'rgba(153, 102, 255, 0.7)',
    'rgba(255, 159, 64, 0.7)',
    'rgba(199, 199, 199, 0.7)',
]

@login_required
def reporte_productos_diarios(request):
    """
    REPORTE RÁPIDO (PARA ENTREGA):
    Muestra un gráfico de Pie con la cantidad de productos por categoría.
    """
    
    # 1. La Consulta (¡Súper simple!)
    # Agrupa por el nombre de la categoría y cuenta cuántos productos hay en cada una
    data_query = (
        Producto.objects
        .values('categoria__nombre')  # Agrupar por nombre de categoría
        .annotate(total=Count('id'))     # Contar productos en ese grupo
        .order_by('-total')              # Ordenar de mayor a menor
    )

    # 2. Preparamos los datos para Chart.js
    labels = []
    data_counts = []
    
    for item in data_query:
        # Si la categoría es Nula, ponle "Sin Categoría"
        nombre = item['categoria__nombre'] or 'Sin Categoría'
        total = item['total']
        
        labels.append(nombre)
        data_counts.append(total)

    # 3. Creamos el 'dataset' para el gráfico de Pie
    datasets = [{
        'label': 'Productos',
        'data': data_counts,
        'backgroundColor': CATEGORIA_COLORES[:len(labels)], # Asigna un color a cada categoría
    }]

    context = {
        'chart_title': 'Productos por Categoría',
        'chart_labels': json.dumps(labels),
        'chart_datasets': json.dumps(datasets),
    }
    
    return render(request, 'reportes/reporte_principal.html', context)