import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from productos.models import Producto
from datetime import date, timedelta

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
    agregados durante la SEMANA ACTUAL (Lunes a Domingo).
    """
    
    tz = timezone.get_current_timezone()
    today_local = timezone.now().astimezone(tz).date() # Fecha local de hoy

    start_of_week = today_local - timedelta(days=today_local.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # 2. La Consulta (MODIFICADA)
    data_query = (
        Producto.objects
        .filter(
            fecha_agregado__gte=start_of_week,
            fecha_agregado__lt=end_of_week + timedelta(days=1) 
        )
        .annotate(dia=TruncDay('fecha_agregado', output_field=models.DateField(), tzinfo=tz))
        .values('dia', 'categoria__nombre')
        .annotate(total=Count('id'))
        .order_by('dia')
    )

    labels = []       # Eje X: ["Lun 10/11", "Mar 11/11", ..., "Dom 16/11"]
    date_map = {}     # Mapa para {<fecha_obj>: "Lun 10/11"}
    
    for i in range(7):
        current_day_date = start_of_week + timedelta(days=i)
        day_str = current_day_date.strftime('%a. %d/%m') # Formato: "Lun. 10/11"
        labels.append(day_str)
        date_map[current_day_date] = day_str

    # Ahora, procesamos los datos de la consulta (que ya están filtrados)
    datos_por_dia = {} # ej: {"Lun. 10/11": {'Lacteos': 2}, "Mie. 12/11": ...}
    nombres_categorias = set() 
    nombres_categorias.add('Sin Categoría')

    for item in data_query:
        dia_date = item['dia'] # Esto es un objeto date()
        if dia_date is None:
            continue
        
        # Usamos el mapa para encontrar la etiqueta de string correcta
        dia_str = date_map.get(dia_date) 
        if not dia_str: # Si el dato no está en nuestro mapa (no debería pasar), lo ignoramos
            continue

        categoria_nombre = item['categoria__nombre'] or 'Sin Categoría'
        total = item['total']
        
        nombres_categorias.add(categoria_nombre)

        if dia_str not in datos_por_dia:
            datos_por_dia[dia_str] = {}
        
        datos_por_dia[dia_str][categoria_nombre] = total

    # 4. Construir los 'datasets' (MODIFICADO)
    datasets = []
    nombres_categorias_lista = sorted(list(nombres_categorias))
    
    for i, nombre_cat in enumerate(nombres_categorias_lista):
        data_para_esta_cat = []
        
        # MODIFICADO: Iteramos sobre las 7 ETIQUETAS, no sobre los datos
        for dia_label in labels:
            # Buscamos el total para este día (ej. "Lun. 10/11") y esta categoría
            # Si no se encuentra, .get() devuelve 0
            total_dia = datos_por_dia.get(dia_label, {}).get(nombre_cat, 0)
            data_para_esta_cat.append(total_dia)
        
        # Solo añadimos el dataset si tiene datos (evita categorías vacías)
        if any(d > 0 for d in data_para_esta_cat):
            datasets.append({
                'label': nombre_cat,
                'data': data_para_esta_cat, # Esta lista siempre tendrá 7 items
                'backgroundColor': CATEGORIA_COLORES[i % len(CATEGORIA_COLORES)],
            })

    context = {
        'chart_labels': json.dumps(labels), # Siempre tendrá 7 etiquetas
        'chart_datasets': json.dumps(datasets),
    }
    
    return render(request, 'reportes/reporte_principal.html', context)