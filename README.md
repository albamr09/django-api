# django-api

## Index

1. [Description](#description)
2. [Technologies used](#technologies)
3. [Principles followed](#principles)
4. [Getting started](#getting_started)
5. [Project Structure](#project_structure)
6. [Setup](#setup_docker)
7. [Project Configuration](#configure_project)
8. [Testing](#testing)
9. [Django Notes](#django_documentation)
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

## Getting started <a name="getting_started"></a>

To start the project run:

```console
$ docker-compose up
```

Once the server is up head to the following url where the API will be available: http://127.0.0.1:8000.

---

## Project Structure <a name="project_structure"></a>

```
django-api
└───app
│   └─── app
│   	 └─── settings.py
│   	 └─── urls.py
│   └─── book
│   	 └─── tests
│   	 └─── apps.py
│   	 └─── serializers.py
│   	 └─── urls.py
│   	 └─── views.py
│   └─── core
│   	 └─── tests
│   	 └─── migrations
│   	 └─── management
│   	 └─── admin.py
│   	 └─── apps.py
│   	 └─── models.py
│   └─── user
│   	 └─── tests
│   	 └─── apps.py
│   	 └─── serializers.py
│   	 └─── urls.py
│   	 └─── views.py
│  .travis.yml 
│  docker-compose.yml 
│  Dockerfile 
│  requirements.txt 
│  README.md 
```

- `app`: contains the global configuration of the project. 
- `core`: Django app that contains the code important to the rest of the subapps on the system.
- `book`: contains the code pertaining the book endpoints.
- `user`: contains the code pertaining the user endpoints.
- `app/settings.py`: contains the global settings for our project.
- `core/migrations`: contains the models modified to follow our models' definitions.
- `core/management`: contains customized management tools (e.g. command to wait for the database to be ready)
- `core/models.py`: contains the definition of all the models (objects) defined on our database.
- `*/tests`: This will contain all of the files with the unit tests for the module.
- `*/apps.py`: Basic information about the app.
- `*/serializers.py`: Serializer classes for the different models defined as to map objects to JSON.
- `*/urls.py`: Definition of the url of the different endpoints defined on the app.
- `*/views.py`: Creation of the views corresponding to the different endpoints of the API.
- `.travis.yml`: `Travis CI` configuration file.
- `docker-compose.yml`: `Docker-compose` configuration file
- `Dockerfile`: Docker image configuration file
- `requirements.txt`: `Python` dependencies

---

## Setup <a name="setup_docker"></a>

Go to the [Set Up](./docs/SetUp.md) documentation page.

## Project Configuration <a name="configure_project"></a>

Go to the [Configuration](./docs/Configuration.md) documentation page.

## Testing <a name="testing"></a>

Go to the [Testing](./docs/Testing.md) documentation page.

## Django Notes <a name="django_documentation"></a>

Go to the [Django Notes](./docs/DjangoDocs.md) page.
