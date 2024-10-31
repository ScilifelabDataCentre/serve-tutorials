---
hide:
  - navigation
---
# Packaging and sharing data science applications as docker container images: Getting Started

This workshop will introduce Docker containers and how you can use them to package applications. By the end of this workshop, we hope you will know how to use Docker on your local machine, package applications with their dependencies, upload the packaged apps to Dockerhub as images. During the workshop we will start with a short talk introducing containers and docker. We will go over the basic commands that you can use to build and run docker containers and expose ports to your local machine.
Then, we will show an example of a shiny application, prepare it for deployment by packaging it as a docker container and make it available on the web with a URL. The target audience of this tutorial are researchers who build applications and tools from different frameworks and want to know about packaging them.

## Step 0. Downloading Docker or Docker Desktop

Docker Desktop is the all-in-one package to build images and run containers.

### Steps to Install Docker Desktop

1. **Download Docker Desktop Installer**  
Visit the Docker Desktop [download page](https://www.docker.com/products/docker-desktop/) and download the installer for your operating system.

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

You have already seen some of these commands but just to refresh, here are the basic docker commands

#### Starting and Stopping

* [`docker start`](https://docs.docker.com/engine/reference/commandline/start) starts a container.
* [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop) stops a running container.
* [`docker restart`](https://docs.docker.com/engine/reference/commandline/restart) stops and re-starts a container.

#### Info

* [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps) shows running containers.
* [`docker logs`](https://docs.docker.com/engine/reference/commandline/logs) gets logs from container.
* [`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect) looks at all the info on a container.
* [`docker top`](https://docs.docker.com/engine/reference/commandline/top) shows running processes in container.

#### Lifecycle

* [`docker images`](https://docs.docker.com/engine/reference/commandline/images) shows all images.
* [`docker build`](https://docs.docker.com/engine/reference/commandline/build) creates image from Dockerfile.
* [`docker run`](https://docs.docker.com/engine/reference/commandline/run) creates and starts a container in one operation.
* [`docker rm`](https://docs.docker.com/engine/reference/commandline/rm) deletes a container.

## Running the hands-on workshop tutorial as a Docker Container

We have built a docker image for the hands-on part of the workshop. The idea is for you to download the image from dockerhub and run it locally on your machine. To do that, make sure docker is installed and running according to the instructions above and then run the following command:

 ```bash
 docker run -p 8000:8000 scilifelabdatacentre/docker-workshop:hands-on
 ```

 You should now have the hands-on tutorial running at <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>.