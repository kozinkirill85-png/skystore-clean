from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    """Главная страница"""
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    """Страница контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Получено сообщение от {name}: {message}")
    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    """Страница одного товара"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})
