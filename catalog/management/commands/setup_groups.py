from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы с необходимыми правами'

    def handle(self, *args, **kwargs):
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем права для модели продукта
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем право на отмену публикации
        unpublish_permission = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )

        # Получаем право на удаление продукта
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        # Добавляем права в группу
        moderator_group.permissions.add(unpublish_permission)
        moderator_group.permissions.add(delete_permission)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана'))
        self.stdout.write(self.style.SUCCESS('Назначены права:'))
        self.stdout.write(f'  - {unpublish_permission.name}')
        self.stdout.write(f'  - {delete_permission.name}')
