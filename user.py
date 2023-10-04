import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "katex.settings")

# Initialize Django
django.setup()

# Now you can import and work with Django models
from katexpower.models import UserProfile

from django.contrib.auth import authenticate

# Replace 'nicholasmaina' with the actual username of your superuser
user = UserProfile.objects.get(username="nicholasmaina")


# Print the password
print(f"Username: {user.username}, Email: {user.email}")
print(user.password)

username = user.email
password_to_check = user.password

user = authenticate(username=username, password=password_to_check)

if user is not None:
    print("Authentication successful.")
    
    # Change the user's password
    new_password = '!Kaniki1234'
    user.set_password(new_password)
    user.save()
    
    print("Password changed successfully.")
else:
    print("Invalid email or password.")