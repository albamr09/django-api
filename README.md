# django-api

## Index

1. [Description](#description)
2. [Technologies used](#technologies)
3. [Principles followed](#principles)
4. [Project Structure](#project_structure)
5. [Setup](#setup_docker)
    1. [Install Docker](#install_docker)
    2. [Configure Docker](#configure_docker)
    3. [Install Docker Compose](#install_compose)
6. [Project Configuration](#configure_project)
    1. [Dockerfile](#dockerfile)
    2. [Dependencies](#requirements)
    3. [Building Docker Image](#build)
    4. [Docker Compose](#configure_compose)
    5. [Create project](#create_project)
    6. [Create core app](#create_core_app)
    7. [Create user app](#create_user_app)
    8. [Create book app](#create_book_app)
    9. [Installed apps](#installed_apps)
    10. [Databases](#databases_django)
    11. [Travis CI](#travis)
    12. [Flake8](#flake8)
7. [Testing](#testing)
8. [Django documentation](#django_documentation)
--- 
## Description <a name="description"></a>

Full fledged REST API that allows you to manage a set of books.

## Technologies used <a name="technologies"></a>


| Name         | Use |
|--------------|-----|
| [**Python 3.7**](https://www.python.org/downloads/release/python-370/) |  Main programming language used to build the API. |
| [**Django**](https://www.djangoproject.com/)      |  Python framework that supports the API. |
| [**Django REST Framework**](https://www.django-rest-framework.org/)      |  Extension to django which adds features related to building APIs. |
| [**Docker**](https://www.docker.com/)      |  Virtualization tool that provides us the mechanism for isolating our project's dependencies from the machine it is running on. |
| [**Travis CI**](https://www.docker.com/)      |  Testing tool for automatically running linting and unit testing every time changes are added to the project's code. |
| [**PostgreSQL**](https://www.postgresql.org/)      |  Database for our project (good integration with docker) |

### Django

Main features used: 
- **ORM**(Object Relational Mapper): provides an easy to use way to convert objects in the API to rows in the database.
- **Django admin**: provides an out-of-the-box website which allows us to manage the objects in our database.

### Django REST Framework

Main features used:
- **Built-in authentication system**: used to add authentication to the API's endpoints.
- **Viewsets**: used to create the structure of the API and create all of the necessary endpoints of the API.
- **Serializers**: provides validation to all of the API's requests and to help convert JSON objects to Django database models.
- **Browsable API**: allowed us to test the API's endpoints on the get-go.

---
## Principles followed <a name="principles"></a>


- [TDD (Test-driven development)](https://en.wikipedia.org/wiki/Test-driven_development)
 1. Write the unit test
 2. Ensure the test fails
 3. Write the feature in order for the test to pass
- [PEP-8 best practice guidelines](https://www.python.org/dev/peps/pep-0008/)

---

## Project Structure <a name="project_structure"></a>

```
django-api
└───app
│   └─── app
│   └─── core
│   	 └─── tests
│  .travis.yml 
│  docker-compose.yml 
│  Dockerfile 
│  requirements.txt 
│  README.md 
```

- `app`: 
- `core`: Django app that contains the code important to the rest of the subapps on the system.
- `core/tests`: This will contain all of the files with the unit tests.
- `.travis.yml`: `Travis CI` configuration file.
- `docker-compose.yml`: `Docker-compose` configuration file
- `Dockerfile`: Docker image configuration file
- `requirements.txt`: `Python` dependencies

---

## Setup <a name="setup_docker"></a>


### Install Docker <a name="install_docker"></a>


In the current section we will lay out the steps to carry out in order to get docker up and running on an Arch Linux machine.

#### Docker engine 

Before installing anything we will update the system as follows

```console
$ sudo pacman -Syu
```

When it is done updating we will proceed rebooting the system, and then we enable the loop module:

```console
$ sudo tee /etc/modules-load.d/loop.conf <<< "loop"
$ sudo modprobe loop
```

##### Install using static binaries

For reference go to the official [documentation](https://docs.docker.com/engine/install/binaries/) on Docker's website. 

1. Firstly we will download the static binary archive on https://download.docker.com/linux/static/stable/. 

2. Once the file is downloaded extract it executing the following command, and substituting our `docker-20.10.8` for your package's version.

```console
$ tar xzvf docker-20.10.8.tgz
```

3. Copy the binaries to your executable path (`/usr/bin` or `/bin`). This is **optional**.


```console
$ sudo cp docker/* /usr/bin/
```

4. Start docker's daemon:

```console
$ sudo dockerd 
```

5. Finally run to check that the installation was correct (it will download an example image that outputs a message informing the user that the installation was successfull, among other things).

```console
$ sudo docker run hello-world
```

#### Official repo

This other approach will allows to have a docker service so we do not have to always run `sudo dockerd &` to start docker's daemon.

1. We install Docker using `pacman`:


```console
$ sudo pacman -S docker 
```

2. Afterwards, we enable the docker service executing:

```console
$ sudo systemctl start docker.service
$ sudo systemctl enable docker.service
```

3. Finally run to check that the installation was correct (it will download an example image that outputs a message informing the user that the installation was successfull, among other things).

```console
$ sudo docker run hello-world
```
### Configure Docker <a name="configure_docker"></a>


#### Running as normal user

In order to use Docker as a normal user we need to add said user to the docker group.

1. Add the Docker group
```console
$ sudo groupadd docker
```
2. Add your user to the Docker group
```console
$ sudo usermod -aG docker $USER
```
3. Log out, log in and verify that it runs properly
```console
$ docker run hello-world
```

### Install Docker Compose <a name="install_compose"></a>

1. Download the current stable release of Docker Compose. Mind you, this command downloads the `1.29.2` version, check the [official page](https://docs.docker.com/compose/install/) for new releases.

```console
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

2. Make the binary executable

```console
$ sudo chmod +x /usr/local/bin/docker-compose
```

3. Test the installation

```console
$ docker-compose --version
docker-compose version 1.29.2, build 5becea4c
```

## Project Configuration <a name="configure_project"></a>

Remember to create the source code folder (`app`), else, when creating the app Docker will exit with error.

### Dockerfile <a name="dockerfile"></a>

First of all, we create a file called `Dockerfile` on the root of our project. In this configuration file we include:

1. **Base image**: It is the image from where we are going to inherit our Dockerfile from, building our image on top of another image. This base image will be downloaded from [Hub Docker](https://hub.docker.com/search?q=&type=image), our image will be created from the python3.7-alpine image (inspect the tags on the python image). 

```dockerfile
FROM $IMAGE:$TAG
```

In our case `IMAGE=python` and `TAG=3.7-alpine`.

2. **Maintainer** (optional): who maintains the docker image.

```dockerfile
MAINTAINER albamr09
```

3. **Environment variables**: in our case we will set an environment variable that prevents Python from keeping outputs in the buffer, so we avoid further complication when working with a Docker image.

```dockerfile
ENV PYTHONUNBUFFERED 1
```

4. **Dependencies**: our dependencies will be listed locally on the file `requirements.txt`, the following line tells Docker to copy this file to the root folder of the Docker machine

```dockerfile
COPY ./requirements.txt /requirements.txt
```

Because in our `requirements.txt` we have included the package that allows for communication to take place between `Postgres` and `Django` we also have to tell `Docker` to install the `PostgreSQL` client. Furthermore, the `jpeg-dev` pakage is needed to make use of images within python, to be more precise, to use the `Pillow` package, referenced lated. For that we include the following line in the config file:

```dockerfile
RUN apk add --update --no-cache postgresql-client jpeg-dev
```

This line executes `apk`, that is alpine's package manager, and install the postgresql-client package. Note that we have added two optional arguments: `--update` (which is abbreviated from `--update-cache`, and updates the package list to get the latest list of available packages), and `--no-cache` (which allows us to not cache the index locally (`/var/cache/apk`) and keeps the container small). 

We also have to install the temporary dependencies related to python dependencies:

```dockerfile
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
```

Observe that we have added the option `--virtual`, which allows us to set up an alias for the temporary dependencies required to install the python dependencies.

Now, in order to install all the python depedencies into the Docker image we use pip, running the next command on the virtual machine:

```dockerfile
RUN pip install -r /requirements.txt
```

Once the python dependecies are installed, we can remove the temporary dependencies by using the alias we specified earlier:

```dockerfile
RUN apk del .tmp-build-deps
```

5. **Application source code**: we create a directory to store our source code, and we tell Docker that this directory is the default directory, and every app will run from said directory

```dockerfile
RUN mkdir /app
WORKDIR /app
COPY ./app /app
```

6. **Media folder creation**: before creating the user, we will create two new folders, one for media that the user uploads (`/vol/web/media`) and one for static files, such as `css` or `javascript` files (`/vol/web/static`). 

```dockerfile
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
```

7. **User creation**: in this step we create the user that will run the application

```dockerfile
RUN adduser -D user
```

8. **Permission management**: note that we also have to give permissions to the user to use the directories we created before, for that we specify:

```dockerfile
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
```


This is done for security porpuses, otherwise the application is run as `root`, which is never recommended.

### Dependencies (Requirements) <a name="requirements"></a>

We, now, specify the dependencies of the project using the file `requirements.txt`. There we abide to the following convention:

```
$PKG>=0.0.1,<1.0.0
```

This way we show that we want to install the python package called `$PKG` whose version is at least `0.0.1` but not more than `1.0.0`.

#### Dependency list

| Name   | Version  |
|--------|:---------:|
| **Django** | >=3.2.7,< 3.3.0 |
| **Django Rest Framework** | >=3.12.4,< 3.13.0 |
| **Flake8** | >=3.9.2, < 3.10.0 |
| **Psycopg2** | >=2.9.1, < 2.10.0 |
| **Pillow** | >=8.3.2,< 8.4.0 |

- `Flake8`: linting tool.
- `psycopg2`: tool that allows Django to communicate with postgres.
- `Pillow`: tool used for manipulating images.

### Building Docker Image <a name="build"></a>

In order to build the Docker image we just configured we must execute, on the root folder of our project (`django-api/`), the following command:

```console
$ docker build .
```

### Docker Compose <a name="configure_compose"></a>

This tool allows us to manage easily the different services (e.g. python app, database, etc.) that make up our project. For that, we will need to make a Docker Compose configuration file denoted by `docker-compose.yml` that sits in the root folder of the project.

On the first line we define the version of Docker Compose for this configuration file:

```yml
version: "3"
```

Next we specify the configuration of the different services:

```yml
services:
  app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manage.py wait_for_db &&
              python manage.py migrate &&
              python manage.py runserver 0.0.0.0:8000"
    environment:
      - DB_HOST=db
      - DB_NAME=app
      - DB_USER=postgres
      - DB_PASS=plaintextpassword
    depends_on:
      - db
```

With this we have:
- Defined the service called app, whose build context will be the `WORKDIR` (`./`). 
- Mapped the port `8000` of our local machine to the port `8000` of the Docker image. 
- For live updating the local changes to our source code to the source code on the Docker image we use `volumes` which maps the local source code folder `./app` to the one on the virtual machine `/app`. 
- In order to run our application in our Docker container we use the keywork `command`. (NOTE: we use `>` so the command is on its own separate line). 
	- First we execute our custom command `wait_for_db`, that is defined on `app/core/management/commands/wait_for_db.py` and that waits for the database to be ready before starting the server. Note that this commands needs to be defined somewhere, else docker-compose will fail to start.
	- Then we migrate our database in case there are any tables that need to be created with `python manage.py migrate`.
	- The command runs the Django development server available on all the IP addresses that run on the Docker container (`0.0.0.0`) on port `8000`, which is mapped to port `8000` in our local machine.
- We also define some environment variables pertaining the database: the service name (`db`), the database name, the database user and its password.
- Next we list our app dependencies, regarding other services. This means that, for example the service `db`, this service will start before the `app` service and the database service will be available on the network when you connect to the hostname `db`.

After that we define the database service:

```yml
  db:
    image: postgres:10-alpine
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=plaintextpassword
```

This database service specifies that docker should pull the `postgres` image with the `10-alpine` tag from the `docker hub`. And then we set some environmental variables: the database name, the user and its password. This password will only be used on the development bulid, on the production build the password would be encrypted.

#### Build

To build our Docker image using the Docker Compose configuration we just put together we execute (remember, on the root folder of the project)

```console
$ docker-compose build
```

#### Run

```console
$ docker-compose up
```

#### Run commands

To run a shell command on our Docker container we use `docker-compose`. This allows us to run the command on the specified service (`app`): 

```console
$ docker-compose run app sh -c "whatever command"
```

The keywords `sh -c ""` are no stricly needed, as the command could be run just with `$ docker-compose run app ""`, however this makes it easier to differentiate the command you are running on the docker image versus the docker-compose command.

We can also add the --rm option to make sure the container does not remained on the system when finished.

```console
$ docker-compose run --rm app sh -c "whatever command"
```

### Create project <a name="create_project"></a>

Now we are going to execute a command to create our project:

```console
$ docker-compose run app sh -c "django-admin.py startproject app ."
```

### Create core app <a name="create_core_app"></a>

To create the core app we must execute:

```console
$ docker-compose run app sh -c "python manage.py startapp core"
```

Once it finishes we remove the files `views.py` and `tests.py` from the core folder, and create a tests folder.

### Create user app <a name="create_user_app"></a>

To create the user app we must execute:

```console
$ docker-compose run app sh -c "python manage.py startapp user"
```

Once it finishes we remove the files `admin.py` and `models.py`, because they are already defined on the `core` app. Then, we also remove the folder `migrations` and the file `tests.py`, and create a tests folder. We also add the `serializers.py` and the `urls.py` files.

### Create book app <a name="create_book_app"></a>

To create the books app we must execute:

```console
$ docker-compose run app sh -c "python manage.py startapp book"
```

Once it finishes we remove the files `admin.py` and `models.py`, because they are already defined on the `core` app. Then, we also remove the folder `migrations` and the file `tests.py`, and create a tests folder. We also add the `serializers.py` and the `urls.py` files.

### Installed apps <a name="installed_apps"></a>

When we have created all the apps necessary, we have to include them inside the installed apps list. For that we head to the `app/app/settings.py` file and specify:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'core',
    'user',
    'book',
]
```

Observe that we have included the necessary django frameworks and modules. To be more precise we have added the `Django Rest Framework` with `rest_framework` and the authetication module with `rest_framework.authtoken`.

### Databases <a name="databases_django"></a>

Once we have set up Docker, we can go ahead and configure our `Django` project to use our `postgres` database. For that we have to head to `app/app/settings.py`, and there we edit the `DATABASES` section as follows:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS')
    }
}
```

Here we tell django that we are going to be using `postgres` as the database manager. The we pull from the environment variables defined within our `Dockerfile` the database's host, name, user and password.

### Static Content and Media

If we want to serve static content o media files, we have to tell `Django` where to serve them. For that we define two variables in `app/app/settings.py` that contain the endpoints within our server that contain static content or media files.

```python
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
```

Then we specify the folders where the content is stored locally so `Django` can map the endpoint with said folder. For that we define:

```python
STATIC_ROOT = '/vol/web/static/'
MEDIA_ROOT = '/vol/web/media/'
```

Finaly on the core url file `app/app/urls.py` we have to specifically tell `Django` to serve media files on the media url endpoint. For that we add `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` to the `urlpattern` variable as follows:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/book/', include('book.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```


### Travis CI <a name="travis"></a>

This continuous integration tool will let us run tests and checks on our project automatically everytime we push to our github repostory. 

1. Sign up to [Travis CI](https://www.travis-ci.com) with your github account.
2. Once you log in, you will be redirected to a [site](https://app.travis-ci.com/getting_started) that will guide you through syncing your repositories.
	1. Click on `ACTIVATE ALL REPOSITORIES USING GITHUB APPS` and select only the repository you with to integrate with Travis CI.
	2. To view the list of selected repositories go to https://app.travis-ci.com/account/repositories. 

#### Configuration file

This file, denoted by `.travis.yml` and located on the project's root directory, tells `Travis CI` what to do when pushing code to the `github` repository.

1. We specify the language we are going to be running Travis CI on

```yml
language: python
```
2. We define the version of `Python` to use:

```yml
python:
  - "3.6"
```

This version differs from the Docker container `python` version, which is `3.7`. However this does not matter because we are only using the Travis CI server to run the Docker image, which has the correct version. 

3. Now we specify the services to use, which will only be docker, the rest of the services are specified within the docker compose config file.

```yml
services:
  - docker
```

4. Next we specify all the actions needed before executing the automated tests:

```yml
before_script: pip install docker-compose
```

5. And finally we run the tests and the linting with docker compose:

```yml
script:
  - docker-compose run app sh -c "python manage.py test && flake8"
```

After this, when we push our changes to the repository, under the `Branches` section for this project's repository, we will be able to see that there is already a build started (it may take some minutes to finish). While it finishes, and when it finishes, it is possible to check the jobs executed by the server under `Job Log`

### Flake8 <a name="flake8"></a>

We will use this linting tool to check whether we are following the `PEP-8` convention. For that we need to specify it as a `Python` dependency (refer to the dependency list) and create a configuration file inside the source code folder (`app/.flake8`).

```
[flake8]
exclude = 
	migrations,
	__pycache__,
	manage.py,
	settings.py
```

With the `exclude` keyword, we tell Flake what directories and files to avoid when running the linting check.


## Testing <a name="testing"></a>

In order to test our unit tests with `Django` we have to take into account the following aspects:

1. The name of the file that contains the text should start with `test` in order to have `Django` pick up that said file contains tests.
2. Also the name of the functions that execute the unit tests should also begin with `test` for the same reason.
3. Every app/subfolder has to have an `__init__.py` in order for it to be picked up by `Django`.

For executing tests we run the following command:

```console
$ docker-compose run app sh -c "python manage.py test"
```

If we also want to include the linting tool we add `flake8` as follows:

```console
$ docker-compose run app sh -c "python manage.py test && flake8"
```


## Django documentation <a name="django_documentation"></a>

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


