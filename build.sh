pip install -r requirements.txt

python manage.py migrate

until python -c "import django; django.setup()" 2>/dev/null; do
  >&2 echo "Waiting for Django to initialize..."
  sleep 1
done

export DJANGO_SETTINGS_MODULE=katex.settings


python <<EOF
import os
import django
from django.contrib.auth.models import User

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'katex.settings')
django.setup()

# Create superuser
def create_superadmin():
    username = 'nicholas'
    email = 'businesskaniki@gmail.com'
    password = '!Kaniki1234'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f'Superuser {username} created successfully!')
    else:
        print(f'Superuser {username} already exists.')

if __name__ == '__main__':
    create_superadmin()
EOF
