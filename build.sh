# Install project dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

python manage.py createsuperuser --noinput --username=reagan  --email=reagan@gmail.com

# Start Django shell and execute Python code to create a superuser with a password
python manage.py shell <<EOF
user = User.objects.get(username='reagan')
user.set_password('!Kaniki1234')
user.save()
EOF

