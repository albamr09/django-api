
## Setup <a name="setup_docker"></a>

### Index

- [Install Docker](#install_docker)
- [Configure Docker](#configure_docker)
- [Install Docker Compose](#install_compose)

---

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
