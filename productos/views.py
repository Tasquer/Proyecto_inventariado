from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Producto, Categoria 
from .forms import ProductoForm, CategoriaForm # Importamos los forms limpios


# --- VISTAS CRUD DE PRODUCTO ---

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/producto_list.html'  
    context_object_name = 'productos'             
    paginate_by = 10                               

class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm 
    template_name = 'productos/producto_form.html' 
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Agregar Nuevo Producto'
        return context
    
    def form_valid(self, form):
        
        messages.success(self.request, 'Producto guardado exitosamente.')
        return super().form_valid(form)


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm 
    template_name = 'productos/producto_form.html' 
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f'Editar: {self.object.nombre}'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return super().form_valid(form)


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('productos:lista')

    def post(self, request, *args, **kwargs):
     
        messages.success(self.request, f'Producto "{self.get_object().nombre}" eliminado.')
        return super().post(request, *args, **kwargs)


# --- VISTA DE CATEGORÍA ---

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/categoria_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Agregar Nueva Categoría'
        return context

    def get_success_url(self):
       
        return reverse_lazy('productos:crear')