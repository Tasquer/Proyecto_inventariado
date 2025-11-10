from django.urls import path
from . import views  


urlpatterns = [
    
    path('', views.DashboardView.as_view(), name='dashboard'),
    # path('reportes/', views.reportes_view, name='reportes'),
]