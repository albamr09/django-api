# django-api

## Index

1. [Description](#description)
2. [Technologies used](#technologies)
3. [Principles followed](#principles)
4. [Setup](#setup_docker)
    1. [Install Docker](#install_docker)
    2. [Configure Docker](#configure_docker)
    3. [Install Docker Compose](#install_compose)
5. [Project Configuration](#configure_project)
    1. [Dockerfile](#dockerfile)
    2. [Dependencies](#requirements)
    3. [Building Docker Image](#build)
    4. [Docker Compose](#configure_compose)
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

## Setup <a name="setup_docker"></a>


### Install Docker <a name="install_docker"></a>


In the current section we will lay out the steps to carry out in order to get docker up and running on an Arch Linux machine.

#### Docker engine 

Before installing anything we will update the system as follows

```bash
$ sudo pacman -Syu
```

When it is done updating we will proceed rebooting the system, and then we enable the loop module:

```bash
$ sudo tee /etc/modules-load.d/loop.conf <<< "loop"
$ sudo modprobe loop
```

##### Install using static binaries

For reference go to the official [documentation](https://docs.docker.com/engine/install/binaries/) on Docker's website. 

1. Firstly we will download the static binary archive on https://download.docker.com/linux/static/stable/. 

2. Once the file is downloaded extract it executing the following command, and substituting our `docker-20.10.8` for your package's version.

```bash
$ tar xzvf docker-20.10.8.tgz
```

3. Copy the binaries to your executable path (`/usr/bin` or `/bin`). This is **optional**.


```bash
$ sudo cp docker/* /usr/bin/
```

4. Start docker's daemon:

```bash
$ sudo dockerd 
```

5. Finally run to check that the installation was correct (it will download an example image that outputs a message informing the user that the installation was successfull, among other things).

```bash
$ sudo docker run hello-world
```

#### Official repo

This other approach will allows to have a docker service so we do not have to always run `sudo dockerd &` to start docker's daemon.

1. We install Docker using `pacman`:


```bash
$ sudo pacman -S docker 
```

2. Afterwards, we enable the docker service executing:

```bash
$ sudo systemctl start docker.service
$ sudo systemctl enable docker.service
```

3. Finally run to check that the installation was correct (it will download an example image that outputs a message informing the user that the installation was successfull, among other things).

```bash
$ sudo docker run hello-world
```
### Configure Docker <a name="configure_docker"></a>


#### Running as normal user

In order to use Docker as a normal user we need to add said user to the docker group.

1. Add the Docker group
```bash
$ sudo groupadd docker
```
2. Add your user to the Docker group
```bash
$ sudo usermod -aG docker $USER
```
3. Log out, log in and verify that it runs properly
```bash
$ docker run hello-world
```

### Install Docker Compose <a name="install_compose"></a>

1. Download the current stable release of Docker Compose. Mind you, this command downloads the `1.29.2` version, check the [official page](https://docs.docker.com/compose/install/) for new releases.

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

2. Make the binary executable

```bash
$ sudo chmod +x /usr/local/bin/docker-compose
```

3. Test the installation

```bash
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

Now, in order to install all of these depedencies into the Docker image we use pip, running the next command on the virtual machine:

```dockerfile
RUN pip install -r /requirements.txt
```

5. **Application source code**: we create a directory to store our source code, and we tell Docker that this directory is the default directory, and every app will run from said directory

```dockerfile
RUN mkdir /app
WORKDIR /app
COPY ./app /app
```

6. **User creation**: in this step we create the user that will run the application

```dockerfile
RUN adduser -D user
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
| **Django** | >= 2.1.3, < 2.2.0|
| **Django Rest Framework** | >= 3.9.0, < 3.10.0|

### Building Docker Image <a name="build"></a>

In order to build the Docker image we just configured we must execute, on the root folder of our project (`django-api/`), the following command:

```bash
$ docker build .
```

### Docker Compose <a name="configure_compose"></a>

This tool allows us to manage easily the different services (e.g. python app, database, etc.) that make up our project. For that, we will need to make a Docker Compose configuration file denoted by `docker-compose.yml` that sits in the root folder of the project that sits in the root folder of the project.

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
      sh -c "python manage.py runserver 0.0.0.0:8000"
```

With this we have:
- Defined the service called app, whose build context will be the `WORKDIR` (`./`). 
- Mapped the port `8000` of our local machine to the port `8000` of the Docker image. 
- For live updating the local changes to our source code to the source code on the Docker image we use `volumes` which maps the local source code folder `./app` to the one on the virtual machine `/app`. 
- Finally, to run our application in our Docker container we use the keywork `command`. (NOTE: we use `>` so the command is on its own separate line). 
	- The command runs the Django development server available on all the IP addresses that run on the Docker container (`0.0.0.0`) on port `8000`, which is mapped to port `8000` in our local machine.

#### Build

To build our Docker image using the Docker Compose configuration we just put together we execute (remember, on the root folder of the project)

```bash
$ docker-compose build
```

#### Create project

To run a shell command on our Docker container we use `docker-compose`. This allows us to run the command on the specified service (`app`): 

```bash
$ docker-compose run app sh -c "django-admin.py startproject app ."
```

The keywords `sh -c ""` are no stricly needed, as the command could be run just with `$ docker-compose run app ""`, however this makes it easier to differentiate the command you are running on the docker image versus the docker-compose command.

The command itself what it does is use `django-admin` (which we installed via dependencies) to create a new project (because we specify `startproject`) with the name `app` in our current location, namely `.` as established on the `Dockerfile` with `WORKDIR`.





