from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя"""
    username = None  # Удаляем поле username

    email = models.EmailField(
        unique=True,
        verbose_name=_('Email'),
        help_text=_('Введите вашу электронную почту')
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name=_('Аватар'),
        help_text=_('Загрузите ваш аватар')
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Номер телефона'),
        help_text=_('Введите ваш номер телефона')
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Страна'),
        help_text=_('Введите вашу страну')
    )

    USERNAME_FIELD = 'email'  # Устанавливаем поле для авторизации
    REQUIRED_FIELDS = []  # Дополнительные обязательные поля

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email
