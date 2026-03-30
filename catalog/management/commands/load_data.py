from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загрузка тестовых данных'

    def handle(self, *args, **kwargs):
        # Удаляем существующие данные
        self.stdout.write('Удаляем существующие данные...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Данные удалены'))

        # Загружаем фикстуры
        self.stdout.write('Загружаем фикстуры...')
        call_command('loaddata', 'categories')
        call_command('loaddata', 'products')
        self.stdout.write(self.style.SUCCESS('Фикстуры загружены'))

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
