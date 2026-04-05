from django.core.cache import cache
from .models import Product
from django.conf import settings

def get_products_by_category(category_id):
    """
    Возвращает список всех продуктов в указанной категории.
    Использует кеширование для повышения производительности.
    """
    if not settings.CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True)

    # Формируем ключ кеша
    cache_key = f'products_by_category_{category_id}'

    # Пытаемся получить данные из кеша
    products = cache.get(cache_key)

    if products is None:
        # Если данных нет в кеше, получаем из базы данных
        products = Product.objects.filter(category_id=category_id, is_published=True)
        # Сохраняем в кеш на 15 минут
        cache.set(cache_key, products, 60 * 15)

    return products
