# Install project dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

python manage.py createsuperuser --noinput --username=reagan123  --email=reagan@gmail123.com

from katexpower.models import UserProfile

# Start Django shell and execute Python code to create a superuser with a password
python manage.py shell <<EOF
user = UserProfile.objects.get(username='reagan')
user.set_password('!Kaniki1234')
user.save()
EOF

