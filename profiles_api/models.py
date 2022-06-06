from django.db import models

# You need to import these two modules if you're planning to overwrite
# on top of default django based models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Import the base model manager
from django.contrib.auth.models import BaseUserManager

# Create your models here.

# We will define functions in this manager class 
# that will manipulate objects of UserProfile class
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """ Create a new user profile and save it in db"""

        if email is None:
            raise ValueError("Users must have a email address")

        email = self.normalize_email(email)

        # Creates a new user model
        user = self.model(email=email, name=name)

        # Setting it this way, password is encrypted
        user.set_password(password)

        # Standard procedure for saving this object in db
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):

        """ Create and save a new super user in db """
        user = self.create_user(email, name, password)

        user.is_superuser= True
        user.is_staff = True
        user.save(using=self._db)

        return user




# By inheriting from these two classes, we'll get default functinality
# of default django user class
# Created a customer user model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    # Define a email field in the model and this has to be unique in the table
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # To determine if the user profile is activated or not
    is_active = models.BooleanField(default=True)
    # To determine if the user is staff
    is_staff = models.BooleanField(default=False)

    # Next we specify the model manager we'll use for the objects
    # We'll be able to interact with the model manager through Django CLI
    # and this manager will create new entries or modify existing entries
    # in our table
    objects = UserProfileManager()

    # This overwrites the default authentication field of username to email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # Define these functions to integrate our model with components in django
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    # Define a function that converts the user object into a string
    def __str__(self):
        """Return string representation of our user"""
        return self.email
