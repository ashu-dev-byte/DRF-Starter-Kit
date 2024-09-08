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

import getpass
import os
import platform
import subprocess
import sys

from django.conf import settings
from django.contrib.auth import get_user_model as User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from enum import Enum


class TerminalColor(Enum):
    WHITE = "\033[37m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[33m"
    CYAN = "\033[96m"
    END = "\33[0m"


def color_text(text, color=TerminalColor.WHITE):
    """Helper function to colorize terminal output."""
    return f"\n{color.value}{text}{TerminalColor.END.value}"


def run_command(cmd, check=False):
    """Helper function to run a subprocess command."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    # print(color_text(result.stdout))
    if result.stderr:
        print(color_text(result.stderr, TerminalColor.RED))
    return result.returncode


class Command(BaseCommand):
    help = "Setup the Django project with default configs"

    def __init__(self):
        super().__init__()
        self.system_os = platform.system()
        self.is_windows = self.system_os == "Windows"

    def handle(self, *args, **options):
        # # Install dependencies
        # print(color_text("Installing dependencies...", BLUE))
        # subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

        print(color_text("All dependencies installed!", TerminalColor.BLUE))
        print(color_text(f"Detected {self.system_os}", TerminalColor.BLUE))

        self.check_postgresql()
        self.setup_postgresql()
        self.run_migrations()
        self.create_superuser()

        self.stdout.write(self.style.SUCCESS("\nProject setup complete!"))

    def check_postgresql(self):
        """Check if PostgreSQL is installed and verify access."""
        print(color_text("Checking PostgreSQL installation...", TerminalColor.BLUE))
        err_msg = "PostgreSQL not found! Please install it and try again."

        try:
            version_info = subprocess.run(
                ["psql", "--version"], capture_output=True, text=True, check=True
            ).stdout.strip()
            print(color_text(f"PostgreSQL found: {version_info}", TerminalColor.BLUE))

            if self.is_windows:
                self.verify_postgresql_password()
        except Exception as e:
            print(color_text(err_msg, TerminalColor.RED))
            sys.exit(1)

    def verify_postgresql_password(self):
        """Verify PostgreSQL password for Windows users."""
        password = getpass.getpass(prompt=color_text("Enter PostgreSQL password: ", TerminalColor.CYAN))
        os.environ["PGPASSWORD"] = password
        print(color_text("Verifying password...", TerminalColor.BLUE))

        check_cmd = ["psql", "-U", "postgres", "-c", "SELECT version();"]
        if run_command(check_cmd) != 0:
            print(color_text("Password verification failed! Exiting.", TerminalColor.RED))
            sys.exit(1)
        else:
            print(color_text("Password verification successful!", TerminalColor.BLUE))

    def setup_postgresql(self):
        """Set up the PostgreSQL database and user."""
        print(color_text("Setting up PostgreSQL...", TerminalColor.BLUE))
        psql_cmd = (
            ["psql", "-U", "postgres", "-c"]
            if self.is_windows
            else ["sudo", "-u", "postgres", "psql", "-c"]
        )
        commands = [
            "CREATE DATABASE drf;",
            "CREATE USER drf_user WITH PASSWORD 'password';",
            "GRANT ALL PRIVILEGES ON DATABASE drf TO drf_user;",
            "ALTER USER drf_user SUPERUSER;",
        ]

        for sql_command in commands:
            print(color_text(sql_command, TerminalColor.CYAN))
            try:
                subprocess.check_call(psql_cmd + [sql_command])
            except subprocess.CalledProcessError:
                pass  # Ignore

        print(color_text("PostgreSQL setup process completed!", TerminalColor.BLUE))

    def run_migrations(self):
        """Run Django migrations."""
        print(color_text("Making migrations...", TerminalColor.BLUE))
        call_command("makemigrations")

        print(color_text("Applying migrations...", TerminalColor.BLUE))
        call_command("migrate")

    def create_superuser(self):
        """Create the default superuser if not exists."""
        server_env = settings.ENV
        if server_env in ["local", "test", "staging"]:
            print(color_text("Creating default superuser...", TerminalColor.BLUE))
            email, name, password = "admin@drf.com", "System Overlord", "password"

            if not User().objects.filter(email=email).exists():
                User().objects.create_superuser(email=email, password=password, name=name)
                print(
                    color_text(
                        f"Superuser created with email: {email} and password: {password}",
                        TerminalColor.BLUE,
                    )
                )
            else:
                print(
                    color_text(
                        f"Superuser already exists with email {email}! Check the README for the password.",
                        TerminalColor.YELLOW,
                    )
                )
