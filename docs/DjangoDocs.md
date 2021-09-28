## Django Notes <a name="django_documentation"></a>

In this section we lay out some concepts about the `Django Framework` pertaining our project.

### Apps

### Models

The models can be thought of as objects, in the sense of OOP, that have certain attributes. This objects are then mapped by Django to the database of choice.
To define new models, or modify existing model (e.g. the user model) you need to modify the `models.py` file in the root folder of every app that is created. Alternatively, you can centralize all of your models on the `core` app.

An example of a simple model is the following `Tag` model:

```python
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
```

Once the model is define, it needs to be registered on the `admin.py` file:

```python
admin.site.register(models.Tag)
```

Specifically when modifying existing models, you will need to extend the classes defined by `Django` (e.g. `AbstractBaseUser`, `UserAdmin`). For example:

```python
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

```

Which has to be registered as follows:

```python
admin.site.register(models.User, UserAdmin)
```

Where `UserAdmin` is a class define in the `admin.py` file, that defines the custom `User` model:

```python
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    # User edit page fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    # User create page fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')
        }),
```

### Admin

This is the feature that allows you to manage your models, let it be create them, modify them or delete them.
The functionality of the admin model is defined within the `admin.py` file on the root folder of every app that is created.

In order to create a superuser execute the following command:

```console
$ python manage.py createsuperuser
```

On Docker:

```console
$ docker-compose run app sh -c "python manage.py createsuperuser"
```

Then, you will be prompted to enter an email and a password. Once you have filled said fields, you can start the server with 


```console
$ docker-compose up
```

And enter to the admin page located on `127.0.0.1:8000/admin`, where you can log in with your credentials.

### URLs

Django allows us to define relative urls on a very modular way. First off, we have the core file when it comes to url definition: `app/app/urls.py`. Here we may have something like this:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
]
```

This example shows that the `urlpatterns` variable is a list that holds all of the urls defined in our project. The modularization comes from the way the urls defined on the user's app are specified. First we specify the endpoint for these urls (namely `api/user/`), and then we pull all the relative urls from the user's app, defined on the file `app/user/urls.py`. Which are then concatenated with `api/user/`. 

The urls defined on the user app are as follows:

```python
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
```

This the can be used like this:

```python
# Create user api endpoint dinamically
CREATE_USER_URL = reverse('user:create')
```

### Serializers

This files are defined to specify how to serialize (map to the database) the JSON objects received, in our case, from HTTP requests. For that we create, for each model, a class that extends `serializers.ModelSerializer`. In this class we define an inner class called `Meta` that tells the framework which fields does the object have and so allows the mapping to take place. You can also add extra arguments to this inner class, for example to restrict or exersise a stronger control on the fields.

Next on, we have a simple example of our User Model serializer:

```python
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        """Info about how to serialize the user model"""
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # Extra requirements for the user model
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # validation_data: JSON data passed in the HTTP POST
        return get_user_model().objects.create_user(**validated_data)
```

We can also serialize an object that is not related to a model per se, for example:

```python
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
```

### Views

This is, on simple terms, a `Python` function that takes a Web request and returns a Web response. In our case, we will mostly use views for our API, so we use pre-make view that allows us to easily make an API that creates, updates, etc an object on the database using the serializer that we specify, for example, the API for creating a user is as follows:

```python
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
```

In case of wanting to update an object we extend `generics.RetrieveUpdateAPIView` instead of `generics.CreateAPIView`. Because this view is private, we need to indicate an authentication mechanism and the level of permissions the user has, in our case the authentication is made via `token` and the permissions are that the user needs to be logged in.

```python
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # Authentication mechanism by which the authentication happens
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user
```

### Actions

- **Start the server** 

Observe that this is executed on the docker-compose config file

```console
$ python manage.py runserver 0.0.0.0:8000
```

- **Sync django settings** (`app/app/settings.py`)

```console
$ python manage.py migrate
```

On docker:

```console
$ docker-compose run app sh -c "python manage.py migrate"
```

- **Sync changes made on models**

```console
$ python manage.py makemigrations
```

On docker:

```console
$ docker-compose run app sh -c "python manage.py makemigrations"
```

You can also specify the name off the app that contains the model

```console
$ python manage.py makemigrations app_name
```
