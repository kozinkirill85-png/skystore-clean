from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.views import View
from django.views.generic.detail import DetailView


class ProductListView(ListView):
    """Список продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Показываем только опубликованные продукты"""
        return Product.objects.filter(is_published=True)


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        """Автоматически устанавливаем владельца продукта"""
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на детальную страницу созданного продукта"""
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование продукта (только для владельца или модератора)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        """Проверяем, что пользователь - владелец продукта или модератор"""
        product = self.get_object()
        return (product.owner == self.request.user) or self.request.user.groups.filter(
            name='Модератор продуктов').exists()

    def get_success_url(self):
        """Перенапление на детальную страницу отредактированного продукта"""
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта (только для владельца или модератора)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'

    def test_func(self):
        """Проверяем, что пользователь - владелец продукта или модератор"""
        product = self.get_object()
        return (product.owner == self.request.user or
                self.request.user.groups.filter(name='Модер продуктов').exists())

    def get_success_url(self):
        """Перенаправление на главную страницу"""
        return reverse('catalog:home')


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Отмена публикации продукта (только для модераторов)"""

    def test_func(self):
        """Проверяем, что пользователь имеет право отменять публикацию"""
        return self.request.user.groups.filter(name='Модератор продуктов').exists()

    def post(self, request, pk):
        """Отменяем публикацию продукта"""
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        messages.success(request, f'Публикация продукта "{product.name}" отменена')
        return redirect('catalog:home')