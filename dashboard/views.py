from django.views.generic import ListView
from productos.models import Producto # Importamos el modelo de la app productos

class DashboardView(ListView):
    """
    Vista para mostrar el panel principal (dashboard) que ahora lista
    los productos y permite buscarlos.
    """
    model = Producto
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'productos'  # Nombre que usaremos en el template
    paginate_by = 10  # Opcional: paginación

    def get_queryset(self):
        """
        Sobrescribimos este método para filtrar por búsqueda 'q' Y
        para ordenar por el parámetro 'sort_by'.
        """
        # 1. Empezamos con la consulta base, optimizada
        queryset = super().get_queryset().select_related('categoria')
        
        # 2. Obtenemos los parámetros de la URL
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')

        # 3. Aplicamos el filtro de búsqueda (si existe)
        if query:
            queryset = queryset.filter(nombre__icontains=query)
            
        # 4. Aplicamos el ordenamiento (sort)
        if sort_by == 'nombre':
            queryset = queryset.order_by('nombre')
        elif sort_by == 'categoria':
            # Ordenamos por el campo 'nombre' del modelo relacionado 'categoria'
            queryset = queryset.order_by('categoria__nombre', 'nombre')
        elif sort_by == 'antiguos':
            queryset = queryset.order_by('fecha_agregado')
        elif sort_by == 'stock':
            # Ordenamos por cantidad (de menor a mayor)
            queryset = queryset.order_by('cantidad', 'nombre')
        else:
            # Por defecto (y si sort_by == 'recientes'), ordenamos por más nuevos
            sort_by = 'recientes' # Aseguramos que 'recientes' sea el valor por defecto
            queryset = queryset.order_by('-fecha_agregado')
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Añadimos el término de búsqueda Y el orden actual
        al contexto.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        
        # Añadimos el 'sort_by' actual al contexto.
        # Si no existe, ponemos 'recientes' como default.
        context['current_sort_by'] = self.request.GET.get('sort_by', 'recientes')
        
        return context