from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.cache import cache
from .models import Product, Category
from .forms import ProductForm


class HomeView(ListView):
    """Главная страница"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Показываем только опубликованные продукты"""
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст"""
        context = super().get_context_data(**kwargs)

        # Пытаемся получить категории из кеша
        categories = cache.get('all_categories')

        # Если в кеше нет, получаем из БД и сохраняем в кеш
        if categories is None:
            categories = Category.objects.all()
            # Сохраняем в кеш на 30 минут
            cache.set('all_categories', categories, 60 * 30)

        context['categories'] = categories
        return context


class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        """Кешируем данные о продукте"""
        obj = super().get_object(queryset)

        if settings.CACHE_ENABLED:
            cache_key = f'product_detail_{obj.pk}'
            cached_obj = cache.get(cache_key)

            # Если в кеше нет, сохраняем объект в кеш
            if cached_obj is None:
                # Сохраняем объект в кеш на 30 минут
                cache.set(cache_key, obj, 60 * 30)
                return obj
            else:
                return cached_obj

        return obj


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
        return (product.owner == self.request.user or
                self.request.user.groups.filter(name='Модератор продуктов').exists())

    def get_success_url(self):
        """Перенаправление на детальную страницу отредактированного продукта"""
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта (только для владельца или модератора)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'

    def test_func(self):
        """Проверяем, что пользователь - владелец продукта или модератор"""
        product = self.get_object()
        return (product.owner == self.request.user or
                self.request.user.groups.filter(name='Модератор продуктов').exists())

    def get_success_url(self):
        """Перенаправление на главную страницу"""
        return reverse('catalog:home')


class CategoryProductsView(ListView):
    """Список продуктов в категории"""
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Получаем продукты по категории с кешированием"""
        category_id = self.kwargs.get('category_id')

        # Формируем ключ кеша
        cache_key = f'products_by_category_{category_id}'

        # Пытаемся получить данные из кеша
        products = cache.get(cache_key)

        if products is None:
            # Если данных нет в кеше, получаем из базы данных
            products = Product.objects.filter(
                category_id=category_id,
                is_published=True
            )
            # Сохраняем в кеш на 15 минут
            cache.set(cache_key, products, 60 * 15)

        return products

    def get_context_data(self, **kwargs):
        """Добавляем информацию о категории в контекст"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(Category, id=category_id)
        return context