import json
from django.core.management.base import BaseCommand
from app_shop.models import Product, Category


class Command(BaseCommand):
    help = "Create data"

    def handle(self, *args, **kwargs):
        with open('category.json', 'r') as json_file:
            json_data = json.load(json_file)
        self.stdout.write("Start creating data")
        for l in json_data:
            Category.objects.create(
                name=l['name'],
                slug=l['slug'],
                parent_category_id=l['parent_category_id'],
            )
            self.stdout.write(f"Категория '{l['name']}' создана")

        self.stdout.write("Stop creating data")
