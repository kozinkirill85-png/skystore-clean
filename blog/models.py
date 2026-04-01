from django.db import models
from django.utils.translation import gettext_lazy as _


class BlogPost(models.Model):
    """Модель блоговой записи"""
    title = models.CharField(
        max_length=255,
        verbose_name=_('Заголовок'),
        help_text=_('Введите заголовок статьи')
    )
    content = models.TextField(
        verbose_name=_('Содержимое'),
        help_text=_('Введите содержимое статьи')
    )
    preview = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        verbose_name=_('Превью (изображение)'),
        help_text=_('Загрузите изображение для статьи')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания'),
        help_text=_('Дата создания статьи')
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Признак публикации'),
        help_text=_('Отметьте, если статья опубликована')
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name=_('Количество просмотров'),
        help_text=_('Количество просмотров статьи')
    )

    class Meta:
        verbose_name = _('Блоговая запись')
        verbose_name_plural = _('Блоговые записи')
        ordering = ['-created_at']

    def __str__(self):
        return self.title