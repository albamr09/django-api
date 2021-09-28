## Project Configuration <a name="configure_project"></a>

### Index

- [Dockerfile](#dockerfile)
- [Dependencies](#requirements)
- [Building Docker Image](#build)
- [Docker Compose](#configure_compose)
- [Create project](#create_project)
- [Create core app](#create_core_app)
- [Create user app](#create_user_app)
- [Create book app](#create_book_app)
- [Installed apps](#installed_apps)
- [Databases](#databases_django)
- [Travis CI](#travis)
- [Flake8](#flake8)

---

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
