from django.core.management.base import BaseCommand

from app_users.user import del_anonymous_users


class Command(BaseCommand):
    help = "Удаление анонимных пользователей"

    def handle(self, *args, **options):
        del_anonymous_users()
