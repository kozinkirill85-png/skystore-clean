from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(
        max_length=255,
        verbose_name=_('Наименование'),
        help_text=_('Введите название категории')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),
        help_text=_('Введите описание категории')
    )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(
        max_length=255,
        verbose_name=_('Наименование'),
        help_text=_('Введите название продукта')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),
        help_text=_('Введите описание продукта')
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name=_('Изображение'),
        help_text=_('Загрузите изображение продукта')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('Категория'),
        help_text=_('Выберите категорию продукта')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Цена за покупку'),
        help_text=_('Введите цену продукта')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания'),
        help_text=_('Дата создания продукта')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата последнего изменения'),
        help_text=_('Дата последнего изменения продукта')
    )

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')

    def __str__(self):
        return self.name
