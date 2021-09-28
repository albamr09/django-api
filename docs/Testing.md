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
