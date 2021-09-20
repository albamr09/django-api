# django-api

Full fledged REST API that allows you to manage a set of books.

## Technologies used

| Name         | Use |
|--------------|-----|
| [**Python 3.7**](https://www.python.org/downloads/release/python-370/) |  Main programming language used to build the API. |
| [**Django**](https://www.djangoproject.com/)      |  Python framework that supports the API. |
| [**Django REST Framework**](https://www.django-rest-framework.org/)      |  Extension to django which adds features related to building APIs. |
| [**Docker**](https://www.docker.com/)      |  Virtualization tool that provides us the mechanism for isolating our project's dependencies from the machine it is running on. |
| [**Travis CI**](https://www.docker.com/)      |  Testing tool for automatically running linting and unit testing every time changes are added to the project's code. |
| [**PostgreSQL**](https://www.postgresql.org/")      |  Database for our project (good integration with docker) |


---
## Principles followed

- [TDD (Test-driven development)](https://en.wikipedia.org/wiki/Test-driven_development)
 1. Write the unit test
 2. Ensure the test fails
 3. Write the feature in order for the test to pass
- [PEP-8 best practice guidelines](https://www.python.org/dev/peps/pep-0008/)

---

## Django

Main features used: 
- **ORM**(Object Relational Mapper): provides an easy to use way to convert objects in the API to rows in the database.
- **Django admin**: provides an out-of-the-box website which allows us to manage the objects in our database.

## Django REST Framework

Main feautures used:
- **Built-in authentication system**: used to add authentication to the API's endpoints.
- **Viewsets**: used to create the structure of the API and create all of the necessary endpoints of the API.
- **Serializers**: to provide validation to all of the API's requests and to help convert JSON objects to Django database models.
- **Browsable API**: which allowed us to test the API's endpoints on the get-go.
