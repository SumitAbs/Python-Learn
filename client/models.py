from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Custom user manager to handle user creation
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name  =   models.CharField(max_length=50)
    last_name   =   models.CharField(max_length=50)
    email       =   models.EmailField(unique=True)
    username    =   models.CharField(max_length=150, unique=True)
    password    =   models.CharField(max_length=255)  # You can use Django's hashing mechanism for storing the password securely
    phone       =   models.CharField(max_length=20, blank=True, null=True)
    address     =   models.TextField(blank=True, null=True)
    
    # Add fields required by Django's authentication system
    is_active   =   models.BooleanField(default=True)  # Used to mark if the user is active
    is_staff    =   models.BooleanField(default=False)  # Whether the user can access the admin site
    is_superuser =  models.BooleanField(default=False)  # Superuser status

    # Necessary fields for authentication system
    USERNAME_FIELD = 'email'  # Email will be used for login
    REQUIRED_FIELDS = ['username']  # You can add fields like 'first_name', 'last_name' here

    objects = UserManager()


    
    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        # You need to implement a method to hash the password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # You need to implement a method to check the hashed password
        return check_password(raw_password, self.password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
