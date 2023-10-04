from django.contrib.auth.models import User


def create_superadmin():
    username = "kachi"
    email = "katexpower@gmail.com"
    password = "kanikikamaa"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser {username} created successfully!")
    else:
        print(f"Superuser {username} already exists.")

if __name__ == '__main__':
    create_superadmin()
