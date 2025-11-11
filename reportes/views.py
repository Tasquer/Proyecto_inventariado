import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from productos.models import Producto, Categoria


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
    
    data_query = (
        Producto.objects
        .values('categoria__nombre')  
        .annotate(total=Count('id'))     
        .order_by('-total')             
    )


    labels = []
    data_counts = []
    
    for item in data_query:
        nombre = item['categoria__nombre'] or 'Sin Categoría'
        total = item['total']
        
        labels.append(nombre)
        data_counts.append(total)

   
    datasets = [{
        'label': 'Productos',
        'data': data_counts,
        'backgroundColor': CATEGORIA_COLORES[:len(labels)], 
    }]

    context = {
        'chart_title': 'Productos por Categoría',
        'chart_labels': json.dumps(labels),
        'chart_datasets': json.dumps(datasets),
    }
    
    return render(request, 'reportes/reporte_principal.html', context)