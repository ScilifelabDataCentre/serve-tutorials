---
hide:
  - navigation
---
# Packaging and sharing data science applications as docker container images: Getting Started

This workshop will introduce Docker containers and how you can use them to package applications. By the end of this workshop, we hope you will know how to use Docker on your local machine, package applications with their dependencies, upload the packaged apps to Dockerhub as images.
Then, we will show an example of a shiny application, prepare it for deployment by packaging it as a docker container and make it available on the web with a URL using Scilifelab Serve. The target audience of this tutorial are researchers who build applications and tools from different frameworks and want to know about packaging them.

## Step 0. Downloading Docker or Docker Desktop

Docker Desktop is the all-in-one package to build images and run containers.

### Steps to Install Docker Desktop

1. **Download Docker Desktop Installer**  
Visit the Docker Desktop <a href="https://www.docker.com/products/docker-desktop/" target="_blank">download page</a> and download the installer for your operating system.

2. **Run the Installer**  

3. **Follow the Installation Wizard**  
Follow the on-screen instructions to complete the installation.

4. **Start Docker Desktop**  
Once the installation is complete, Docker Desktop will start automatically.You can also start it manually.

5. **Verify Installation**  
Open a terminal (Command Prompt, PowerShell, or any other terminal) and run the following command to verify the installation:
 ```sh
 docker --version
 ```
You should see the Docker version information displayed.

6. **Run a Test Container**  
To ensure Docker is working correctly, run a test container:
 ```sh
 docker run hello-world
 ```
This command downloads a test image and runs it in a container. If successful, you will see a message indicating that Docker is installed correctly.

---

By following these steps, you should have Docker Desktop installed and running on your system. If you have any questions or run into issues, feel free to ask!

## Basic Docker commands

Here are some basic docker commands that will help you during the hands-on session.

#### Lifecycle

* [`docker images`](https://docs.docker.com/engine/reference/commandline/images){:target="_blank"} shows all images.
```console
docker images
```
* [`docker build`](https://docs.docker.com/reference/cli/docker/build-legacy/){:target="_blank"} creates image from Dockerfile.
```console
docker build -t <image-name>:<tag> .
```
* [`docker run`](https://docs.docker.com/engine/reference/commandline/run){:target="_blank"} creates and starts a container in one operation.
```console
docker run -p <host-port>:<container-port> <image-name>:<tag>
```

#### Info

* [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps){:target="_blank"} shows running containers.
```console
docker ps
```
* [`docker logs`](https://docs.docker.com/engine/reference/commandline/logs){:target="_blank"} gets logs from a running container.
```console
docker logs <container-name>
```
* [`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect){:target="_blank"} looks at all the info on a container.
```console
docker inspect <container-name>
```
* [`docker top`](https://docs.docker.com/engine/reference/commandline/top){:target="_blank"} shows running processes in container.
```console
docker top <container-name> 
```

#### Starting and Stopping

* [`docker start`](https://docs.docker.com/engine/reference/commandline/start){:target="_blank"} starts a container.
```console
docker start <container-name>
```
* [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop){:target="_blank"} stops a running container.
```console
docker stop <container-name>
```
* [`docker restart`](https://docs.docker.com/engine/reference/commandline/restart){:target="_blank"} stops and re-starts a container.
```console
docker restart <container-name>
```


## Create an account on Dockerhub and Sign In

As part of this workshop, you will create a Docker Image and push to it Docker's Image Regsitry called Dockerhub. To do this, you need to create a docker account, which you can do by going to their <a href="https://hub.docker.com/" target="_blank">website</a> and creating an account. Once this is done, you can go to the terminal on your computer and run the following command:

```console
docker login
```

## Running the hands-on workshop tutorial as a Docker Container

We have built a docker image for the hands-on part of the workshop. The idea is for you to download the image from dockerhub and run it locally on your machine. To do that, make sure docker is installed and running according to the instructions above and then run the following command:

 ```bash
 docker run -p 8000:8000 scilifelabdatacentre/docker-workshop:hands-on
 ```

 You should now have the hands-on tutorial running at <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>.