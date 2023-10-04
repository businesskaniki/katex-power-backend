# Install project dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser with a specified username and email
python manage.py createsuperuser --noinput --username=kachi2032 --email=kachi32@gmail.com

# Start Django shell and execute Python code to set the password for the superuser
python manage.py shell <<EOF
from katexpower.models import UserProfile

# Replace 'kachi2032' and '!Kaniki1234' with your desired username and password
username = 'kachi2032'
password = '!Kaniki1234'

try:
    user = UserProfile.objects.get(username=username)
except UserProfile.DoesNotExist:
    user = None

if user:
    user.set_password(password)
    user.save()
    print(f'Password for superuser {username} has been set successfully.')
else:
    print(f'Superuser with username {username} not found.')

EOF
