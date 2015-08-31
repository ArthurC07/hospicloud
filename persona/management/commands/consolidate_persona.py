from django.core.management.base import BaseCommand
from persona.models import remove_duplicates


class Command(BaseCommand):
    help = "Consolidate duplicate persona"

    def handle(self, *args, **options):
        remove_duplicates()
