# reportes/views.py
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# 👇 1. ¡AQUÍ ESTÁ LA CORRECCIÓN!
# Importamos 'models' desde 'django.db' y 'Count' desde 'django.db.models'
from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDay
from productos.models import Producto

# Define una paleta de colores para las categorías
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
    Prepara los datos para el gráfico de barras apiladas de productos
    agregados por día y por categoría.
    """
    
    # 1. La Consulta (El corazón de la lógica)
    data_query = (
        Producto.objects
        # 👇 2. Esta parte ya estaba bien y usa 'models.DateField()'
        .annotate(dia=TruncDay('fecha_agregado', output_field=models.DateField()))
        .values('dia', 'categoria__nombre')       # Agrupa por día y nombre de categoría
        .annotate(total=Count('id'))              # Cuenta los productos en ese grupo
        .order_by('dia')                          # Ordena por día
    )

    # 2. Transformación de datos (para Chart.js)
    labels = []       # Eje X: Los días (ej. 'Lunes 10/11')
    datos_por_dia = {} # ej: {'Lunes 10/11': {'Lacteos': 2, 'Chocolate': 1}}
    
    # Obtenemos todos los nombres de categorías únicos
    nombres_categorias = list(Producto.objects.values_list('categoria__nombre', flat=True).distinct())
    nombres_categorias.append('Sin Categoría') # Para productos sin categoría

    for item in data_query:
        
        # --- 👇 ¡ESTA ES LA CORRECCIÓN! 👇 ---
        # Si 'dia' es None (porque 'fecha_agregado' era NULL),
        # nos saltamos este registro para evitar el error.
        if item['dia'] is None:
            continue
        # --- FIN DE LA CORRECCIÓN ---

        # Formateamos el día (ej. 'lun. 10/11/25')
        dia_str = item['dia'].strftime('%a. %d/%m/%y') # Ahora esta línea es segura
        categoria_nombre = item['categoria__nombre'] or 'Sin Categoría'
        total = item['total']
        
        if dia_str not in datos_por_dia:
            datos_por_dia[dia_str] = {}
            labels.append(dia_str) # Añade la etiqueta del día solo una vez
        
        # Guarda el total para esa categoría en ese día
        datos_por_dia[dia_str][categoria_nombre] = total

    # 3. Construir los 'datasets' que Chart.js necesita
    datasets = []
    
    for i, nombre_cat in enumerate(nombres_categorias):
        data_para_esta_cat = []
        
        # Para cada día en nuestras etiquetas...
        for dia_label in labels:
            # ...busca el total para esta categoría (o pon 0 si no hubo)
            total_dia = datos_por_dia.get(dia_label, {}).get(nombre_cat, 0)
            data_para_esta_cat.append(total_dia)
        
        # Solo añade el dataset si tiene datos (evita categorías vacías)
        if any(d > 0 for d in data_para_esta_cat):
            datasets.append({
                'label': nombre_cat,
                'data': data_para_esta_cat,
                'backgroundColor': CATEGORIA_COLORES[i % len(CATEGORIA_COLORES)],
            })

    context = {
        # Usamos json.dumps para pasar los datos de Python a JavaScript de forma segura
        'chart_labels': json.dumps(labels),
        'chart_datasets': json.dumps(datasets),
    }
    
    return render(request, 'reportes/reporte_principal.html', context)