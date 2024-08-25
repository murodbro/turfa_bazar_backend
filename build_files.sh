#!/bin/bash

# Activate the virtual environment
source /path/to/your/venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create a superuser
echo "from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(email='murodjon@gmail.com').exists():
    User.objects.create_superuser('murodjon@gmail.com', '571632')
" | python manage.py shell

echo "Superuser created with email: murodjon@gmail.com and password: 571632"
