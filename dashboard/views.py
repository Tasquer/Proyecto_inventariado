from django.views.generic import ListView
from productos.models import Producto

class DashboardView(ListView):
    """
    Vista para mostrar el panel principal (dashboard) que ahora lista
    los productos y permite buscarlos.
    """
    model = Producto
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'productos'  
    paginate_by = 10 

    def get_queryset(self):
        """
        Sobrescribimos este método para filtrar por búsqueda 'q' Y
        para ordenar por el parámetro 'sort_by'.
        """
        queryset = super().get_queryset().select_related('categoria')
        
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')


        if query:
            queryset = queryset.filter(nombre__icontains=query)
            
        if sort_by == 'nombre':
            queryset = queryset.order_by('nombre')
        elif sort_by == 'categoria':
            queryset = queryset.order_by('categoria__nombre', 'nombre')
        elif sort_by == 'antiguos':
            queryset = queryset.order_by('fecha_agregado')
        elif sort_by == 'stock':
            queryset = queryset.order_by('cantidad', 'nombre')
        else:

            sort_by = 'recientes' 
            queryset = queryset.order_by('-fecha_agregado')
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Añadimos el término de búsqueda Y el orden actual
        al contexto.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        
        context['current_sort_by'] = self.request.GET.get('sort_by', 'recientes')
        
        return context