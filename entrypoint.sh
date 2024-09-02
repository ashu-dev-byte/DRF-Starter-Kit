#!/bin/bash
# Entry point script to handle migrations, collectstatic, and superuser creation

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

username = 'admin'
email = 'admin@drf.com'
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

User = get_user_model()

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
" || echo "Superuser already exists."

# Start the application
exec "$@"
