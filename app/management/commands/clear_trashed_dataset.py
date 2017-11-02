from django.core.management.base import BaseCommand, CommandError
from app.models import Dataset

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        trashed = Dataset.objects.filter(trashed = True)
        self.stdout.write("Num in trash bin: %i" % len(trashed))
        self.stdout.write("Start clearing...")
        trashed.delete()
        self.stdout.write("Finished clearing...")
