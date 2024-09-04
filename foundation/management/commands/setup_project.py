"""
subprocess.check_call
----------------------
Runs an external command and waits for it to complete.
Raises CalledProcessError if the command exits with a non-zero status.
Example: subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

subprocess.run
--------------
Executes a command and waits for it to complete.
Returns a CompletedProcess instance with return code, stdout, and stderr.
Use 'check=True' to raise an exception on non-zero exit status.
Example: result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

call_command
------------
Executes Django management commands within the Django framework.
Example: call_command('migrate')
"""

from django.contrib.auth import get_user_model as User
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
import subprocess


WHITE, YELLOW, BLUE, GREEN, CYAN = "\033[37m", "\033[33m", "\033[94m", "\033[92m", "\033[96m"
END = "\33[0m"


def color_text(text, color=WHITE):
    return f"{color} {text} {END}"


class Command(BaseCommand):
    help = "Setup the Django project with default configs"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(color_text("Starting project setup:", CYAN)))

        print(color_text("\nInstalling dependencies...", BLUE))
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

        print(color_text("\nMaking migrations...", BLUE))
        call_command("makemigrations")

        print(color_text("\nApplying migrations...", BLUE))
        call_command("migrate")

        server_env = settings.ENV
        if server_env in ["local", "test", "staging"]:
            self.stdout.write(color_text("\nCreating default superuser...", BLUE))
            email = "orgAdmin@afterSkool.com"
            name = "Organization Admin"
            password = "password"
            if not User().objects.filter(email=email).exists():
                User().objects.create_superuser(email=email, password=password, name=name)
                print(color_text("Superuser created successfully!", BLUE))
            else:
                print(color_text("Superuser already exists!", YELLOW))

        self.stdout.write(self.style.SUCCESS("\nProject setup complete!"))
