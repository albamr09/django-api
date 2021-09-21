# django-api

## Index

1. [Description](#description)
2. [Technologies used](#technologies)
3. [Principles followed](#principles)
4. [Setup](#setup_docker)
    1. [Install Docker](#install_docker)
    2. [Configure Docker](#configure_docker)
    3. [Install Docker Compose](#install_compose)
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

1. Download the current stable release of Docker Compose. Mind you, this command download the `1.29.2` version, check the [official page](https://docs.docker.com/compose/install/) for new releases.

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

