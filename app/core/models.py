import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.conf import settings


def year_choices():
    """ Helper fuction for creating a list of possible publication years"""
    return [(r, r) for r in range(1500, datetime.date.today().year+1)]


def current_year():
    """ Helper fuction for retrieving the current year"""
    return datetime.date.today().year


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a book"""
    # Define the attributes of the table
    name = models.CharField(max_length=255)
    # Define the relation between the tag and the user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # Define the string representation of the Tag
    def __str__(self):
        return self.name


class Author(models.Model):
    """Author of a book"""
    # Define the attributes of the table
    name = models.CharField(max_length=255)
    # Define the relation between the tag and the user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # Define the string representation of the Author
    def __str__(self):
        return self.name


class Book(models.Model):
    """Book object"""
    # Define books attributes
    # To define a manytoOne relationship we use a
    # foreign key
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    pages = models.IntegerField()
    year = models.IntegerField(choices=year_choices(), default=current_year)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    authors = models.ManyToManyField('Author')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
