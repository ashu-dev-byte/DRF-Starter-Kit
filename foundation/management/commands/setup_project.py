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

import platform
import subprocess
import sys

WHITE, YELLOW, BLUE, GREEN, CYAN = "\033[37m", "\033[33m", "\033[94m", "\033[92m", "\033[96m"
END = "\33[0m"


def color_text(text, color=WHITE):
    return f"\n{color}{text}{END}"


class Command(BaseCommand):
    help = "Setup the Django project with default configs"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(color_text("Dependencies installed! Starting further process:", CYAN))
        )

        # Install dependencies
        # print(color_text("Installing dependencies...", BLUE))
        # subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

        system_os = platform.system()
        is_windows = system_os == "Windows"
        print(color_text(f"Detected {system_os}", BLUE))

        # Check if PostgreSQL is installed
        print(color_text("Checking PostgreSQL installation...", BLUE))
        try:
            unix_postgres = ["which", "psql"]
            windows_postgres = ["where", "psql"]
            find_postgres = windows_postgres if is_windows else unix_postgres
            result = subprocess.run(find_postgres, capture_output=True, text=True, check=True)
            if not result.stdout.strip():
                self.stdout.write(
                    self.style.ERROR(
                        "\nPostgreSQL is not installed. Please install PostgreSQL and try again.",
                    )
                )
                sys.exit(1)

            # Log PostgreSQL version
            version_result = subprocess.run(
                ["psql", "--version"], capture_output=True, text=True, check=True
            )
            version_info = version_result.stdout.strip()
            print(color_text(f"PostgreSQL found: {version_info}", BLUE))
        except subprocess.CalledProcessError:
            self.stdout.write(
                self.style.ERROR("\nNot found! Ensure PostgreSQL is installed and accessible.")
            )
            sys.exit(1)

        # Set up PostgreSQL
        print(color_text("Setting up PostgreSQL...", BLUE))
        unix_psql = ["sudo", "-u", "postgres", "psql", "-c"]
        windows_psql = ["psql", "-c"]
        psql_cmd = windows_psql if is_windows else unix_psql
        commands = [
            "CREATE DATABASE drf;",
            "CREATE USER drf_user WITH PASSWORD 'password';",
            "GRANT ALL PRIVILEGES ON DATABASE drf TO drf_user;",
            "ALTER USER drf_user SUPERUSER;",
        ]
        FAILED = False

        for sql_command in commands:
            try:
                print(color_text(f"{sql_command}", CYAN))
                subprocess.check_call(psql_cmd + [sql_command])
            except subprocess.CalledProcessError as e:
                FAILED = True

        if not FAILED:
            print(color_text("PostgreSQL setup process completed!", BLUE))

        # Run migrations
        print(color_text("Making migrations...", BLUE))
        call_command("makemigrations")

        print(color_text("Applying migrations...", BLUE))
        call_command("migrate")

        # Create superuser
        server_env = settings.ENV
        if server_env in ["local", "test", "staging"]:
            self.stdout.write(color_text("Creating default superuser...", BLUE))
            email = "admin@drf.com"
            name = "System Overlord"
            password = "password"
            if not User().objects.filter(email=email).exists():
                User().objects.create_superuser(email=email, password=password, name=name)
                print(color_text("Superuser created successfully!", BLUE))
            else:
                print(color_text("Superuser already exists!", YELLOW))

        self.stdout.write(self.style.SUCCESS("\nProject setup complete!"))
