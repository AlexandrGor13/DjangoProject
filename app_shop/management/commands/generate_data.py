import json
from django.core.management.base import BaseCommand
from app_shop.models import Product, Category


class Command(BaseCommand):
    help = "Create data"

    def handle(self, *args, **kwargs):
        with open('app_shop/management/commands/category.json', 'r') as json_file:
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

        with open('app_shop/management/commands/products.json', 'r') as json_file:
            json_data = json.load(json_file)
        self.stdout.write("Start creating data")
        for l in json_data:
            Product.objects.create(
                title=l['title'],
                specifications=l['specifications'],
                description=l['description'],
                price=l['price'],
                discount=l['discount'],
                stock_quantity=l['stock_quantity'],
                img=l['img'],
                is_active=l['is_active'],
                category=Category.objects.filter(id=l['category_id']).first(),
            )
            self.stdout.write(f"Товар '{l['title']}' создана")

        self.stdout.write("Stop creating data")
