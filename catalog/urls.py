# catalog/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Product

class HomeView(ListView):
    """Главная страница"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'

# Остальные классы (ProductDetailView и т.д.)