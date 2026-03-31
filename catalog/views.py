from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.shortcuts import render
from .models import Product


class HomeView(ListView):
    """Главная страница"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(View):
    """Страница контактов"""

    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Получено сообщение от {name}: {message}")
        return render(request, 'catalog/contacts.html')


class ProductDetailView(DetailView):
    """Страница одного товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
