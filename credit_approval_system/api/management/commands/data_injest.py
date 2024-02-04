from typing import Any
from django.core.management.base import BaseCommand
from api.tasks import ingest_data


class Command(BaseCommand):
    help = "Ingest data using Celery"

    def handle(self, *args: Any, **options: Any):
        self.stdout.write(self.style.SUCCESS("Running Data ingestion task..."))
        ingest_data.delay()
        self.stdout.write(self.style.SUCCESS("Task queued Successfully."))
