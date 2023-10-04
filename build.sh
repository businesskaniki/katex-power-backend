# Install project dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

python manage.py createsuperuser --noinput --username=kachi2032  --email=kachi32@gmail.com


# Start Django shell and execute Python code to create a superuser with a password
python manage.py shell <<EOF
    from katexpower.models import UserProfile
    user = UserProfile.objects.get('kachi2032')
    user.set_password('!Kaniki1234')
    user.save()
EOF

