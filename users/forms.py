from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'phone', 'country', 'avatar')
        labels = {
            'email': 'Email',
            'phone': 'Номер телефона',
            'country': 'Страна',
            'avatar': 'Аватар',
        }

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Особая стилизация для поля аватара
        if 'avatar' in self.fields:
            self.fields['avatar'].widget.attrs['class'] = 'form-control-file'

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')

        return email