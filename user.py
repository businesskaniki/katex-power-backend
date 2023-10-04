import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "katex.settings")

# Initialize Django
django.setup()

# Now you can import and work with Django models
from katexpower.models import UserProfile


# Replace 'nicholasmaina' with the actual username of your superuser
user = UserProfile.objects.get(username="nicholasmaina")


# Print the password
print(f"Username: {user.username}, Email: {user.email}")
print(user.password)
