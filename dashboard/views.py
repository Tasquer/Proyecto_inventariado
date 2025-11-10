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
        Sobrescribimos este método para filtrar por el parámetro de búsqueda 'q'.
        """
        # Usamos select_related para optimizar la consulta a la BD,
        # ya que también pediremos la categoría en el template.
        queryset = super().get_queryset().select_related('categoria').order_by('-fecha_agregado')
        
        # Obtenemos el valor del parámetro 'q' de la URL (GET)
        query = self.request.GET.get('q') 
        
        if query:
            # Si hay una búsqueda, filtramos el queryset por nombre
            # Usamos __icontains para que no sea sensible a mayúsculas/minúsculas
            queryset = queryset.filter(nombre__icontains=query)
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Añadimos el término de búsqueda al contexto para poder
        mostrarlo en el input del formulario.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context