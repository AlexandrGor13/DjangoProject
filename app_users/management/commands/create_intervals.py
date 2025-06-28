import json
from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule


class Command(BaseCommand):
    help = "Create intervals"

    def handle(self, *args, **kwargs):
        with open("app_users/management/commands/intervals.json", "r") as json_file:
            json_data = json.load(json_file)
        self.stdout.write("Start creating intervals")
        for l in json_data:
            IntervalSchedule.objects.create(
                every=l["every"],
                period=l["period"],
            )
            self.stdout.write(f"Interval '{l['every']} {l['period']}' created")
        self.stdout.write("Stop creating intervals")
