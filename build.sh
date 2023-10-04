# Install project dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start Django shell and execute Python code to create a superuser with a password
python manage.py shell <<EOF
from katexpower.models import UserProfile

# Replace these values with your desired username, email, and password
username = 'nicholaskamu'
email = 'businesskaniki23@gmail.com'
password = '!Kaniki1234'

try:
    user = UserProfile.objects.get(username=username)
except User.DoesNotExist:
    user = None

if not UserProfile:
    user = UserProfile.objects.create_user(username=username, email=email)
    user.set_password(password)
    user.save()
    print(f'Superuser {username} created successfully with the specified password.')
else:
    print(f'A user with the username {username} already exists.')

EOF

