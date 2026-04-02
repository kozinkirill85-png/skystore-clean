from django import forms
from .models import Product

# Список запрещенных слов
BANNED_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена за покупку',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Особая стилизация для поля изображения
        if 'image' in self.fields:
            self.fields['image'].widget.attrs['class'] = 'form-control-file'

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data.get('name', '')

        # Проверяем каждое запрещенное слово
        for word in BANNED_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(
                    f'Название не должно содержать запрещенное слово: "{word}"'
                )

        return name

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data.get('description', '')

        # Проверяем каждое запрещенное слово
        for word in BANNED_WORDS:
            if word.lower() in description.lower():
                raise forms.ValidationError(
                    f'Описание не должно содержать запрещенное слово: "{word}"'
                )

        return description

    def clean_price(self):
        """Валидация цены на отрицательное значение"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise forms.ValidationError(
                'Цена не может быть отрицательной'
            )

        return price
