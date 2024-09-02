from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "For testing and debugging purposes."

    def handle(self, *args, **kwargs):
        print(f'Project DRF Starter Kit: \n{"="*24}')
