from django.contrib.auth.models import User

# Replace 'nicholasmaina' with the actual username of your superuser
user = User.objects.get(username='nicholasmaina')

# Print the password
print(user.password)