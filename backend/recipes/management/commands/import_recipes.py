import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Запуск загрузки ингридиентов'))
        with open('data/ingredients.json', encoding='utf-8') as ingredients_file:
            ingredients_json = json.load(ingredients_file)
            for ingredient_data in ingredients_json:
                Ingredient.objects.get_or_create(**ingredient_data)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
