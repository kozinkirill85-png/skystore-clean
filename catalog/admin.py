from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Category"""
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)

    def get_readonly_fields(self, request, obj=None):
        """Поля, которые нельзя редактировать"""
        return ('created_at', 'updated_at') if obj else ()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для модели Product"""
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def get_readonly_fields(self, request, obj=None):
        """Поля, которые нельзя редактировать"""
        return ('created_at', 'updated_at') if obj else ()
