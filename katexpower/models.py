from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("please provde an email pleasee")
        if not username:
            raise ValueError("yoow you have to provide a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def defualt_profile():
    return "images/profile/defualts/defualt_profile.png"


def defualt_backgroung():
    return "images/profile/defualts/defualt_background.png"


def defualt_profile_frame():
    return "images/profile/defualts/defualt_frame.png"


class UserProfile(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=200, verbose_name="email")
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    profilepic = models.ImageField(upload_to='profiles/', null=True, blank= True, default="profiles/defualt.png")
    is_writer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

        # Does this user have permission to view this app? (ALWAYS YES FOR
        # SIMPLICITY)

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogs/', null=True, blank= True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def author_username(self):
        return self.author.username

    @property
    def author_first_name(self):
        return self.author.first_name

    @property
    def author_last_name(self):
        return self.author.last_name
    
    @property
    def author_picture(self):
        return self.author.profilepic
   

    @property
    def is_writer(self):
        return self.author.is_writer
