---
hide:
  - navigation
---
# Packaging and sharing data science applications as docker container images: Hands-on

!!! info
    If you have already installed Docker desktop and have tried basic docker commands, you can start at Step 1.

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


## Step 1. Building a basic image and publishing to Dockerhub

In this section we will build a docker image and then publish it to Dockerhub.

### Basic Python app

We start with a basic python flask app. Flask is a lightweight and flexible framework for web development and web applications based on Python. To create this application we will have to create the following files with the following file structure

```bash
..
├── requirements.txt
├── app.py
└── Dockerfile
```

Create a directory named `flask-web-app` on your computer in a location where you want to have it.

Then, in this directory create the files mentioned above. The files will look as follows
```python
# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Welcome to the Docker Workshop. I am Flask!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
```bash
# requirements.txt
Flask
```
```docker
# Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY app.py /app
EXPOSE 5000
CMD ["python", "app.py"]
```

Once all of these files are created, we can move onto building the docker image. 

### Build your Docker Image

Ensure that Docker Desktop is running. Open Terminal and navigate to the folder where your app files and the Dockerfile are located.

```bash
cd path/to/your/folder
```

Run the Docker command to build your image as shown below. Building the image may take a while.

!!! warning  "Note"
    The dot **(.)** at the end of the command is important. This sets the build context to the current directory. This means that the build expects to find the Dockerfile in the directory where the command is invoked

```bash
docker build -t <some-name>:<some-tag> .
```
Replace `<some-name>:<some-tag>` with the name of the app and some tag to identify this particular version. For instance `my-web-app:v2`. 
Once the process is complete, run the following command in the Terminal. You should see your image in the list.

```bash
docker images
```

In order to test that the image you just built works you need to run a container from this image. To do that, run the following command in the Terminal.

```bash
docker run -p <local-port>:<container-port> <some-name>:<some-tag>
```

If everything went well, you should now be able to navigate to `http://localhost:<local-port>` in your browser and see and interact with your app.

??? "Click to see exact commands"
    Run the following command to build the docker container
    !!! warning  "Note"
        The dot **(.)** at the end of the command is important. This sets the build context to the current directory. This means that the build expects to find the Dockerfile in the directory where the command is invoked
    ```bash
    docker build -t flask-web-app .
    ```
    !!! tip "Pro tip"
        It is a good idea to use your Dockerhub username name when building and tagging images as this makes it possible to push images to an image registry such as Dockerhub.
        Using versioning is very helpful as well.
        As an example, the command above could be written as:
        ```
        docker build -t <your-dockerhub-username>/flask-web-app:v1.0.0 .
        ```
    After building the image you can then run it with the following command

    ```bash
    docker run -p 5000:5000 flask-web-app
    ```

    Once it is running you should see that it is available under <a href="http://localhost:5000" target="_blank">http://localhost:5000</a> (or see what Flask tells you in the terminal window, it should say "Running on URL: ..."). Navigate to this link in your browser and try out the app.

    !!! tip "Pro tip"
        It is often useful to run the container in detached mode so that it can run in the background.
        As an example, the command above could be written as:
        ```bash
        docker run -d -p 5000:5000 flask-web-app
        ```

### Publish your Docker Image

You have now built and tested an image for your app on your computer. In order to be able to host this image on SciLifeLab Serve it needs to be published in a so-called image registry. Below, we show how to publish your image on [DockerHub](https://hub.docker.com) as an example but you can choose any public image registry (for example, on GitHub).

Register on [DockerHub](https://hub.docker.com/) and sign in with your account on Docker Desktop app.


Next, re-build your image as described above, this time including your DockerHub username in the image name, as shown below. 

!!! warning  "Note"
    The dot **(.)** at the end of the command is important. This sets the build context to the current directory. This means that the build expects to find the Dockerfile in the directory where the command is invoked

```bash
docker build -t <your-dockerhub-username>/<some-name>:<some-tag> .
```

Once the image is built and visible on Docker Desktop, pick *"Push to Hub"* among the options for your app image. Alternatively, you can also use the following command from the terminal instead

```bash
docker push <your-dockerhub-username>/<some-name>:<some-tag>
```

Keep in mind the you might need to login to you DockerHub user in case you haven't done so already. This can be done as follows:

```bash
docker login
```

This should publish your image on `https://hub.docker.com/r/<your-dockerhub-username>/<some-name>`. For example, our example app image for the flask web app is available at `scilifelabdatacentre/workshop-flask-web-app`.

## Step 2. Packaging a shiny application as a Docker Container Image to deploy on Scilifelab Serve

In this section we will download code for a shiny application, add a Dockerfile and build a Docker image. This image will be built according to the requirements to host it on Scilifelab Serve. This section assumes that you have git installed on your system.

In your terminal, run the follow command

```bash
git clone https://github.com/ScilifelabDataCentre/shiny-adhd-medication-sweden.git -b container-workshop
```

then, run the command

```bash
cd shiny-adhd-medication-sweden
```

In this folder, we will have the Shiny app code in a file called `app.R` and this file as well as the app's dependencies (e.g., associated data) are located in the folder called `app`. 

The app is a dashboard plotting the number of people in Sweden aged 0-19 who have have filled a prescription for ADHD medication each year. The dashboard is based on open data from the *The Swedish National Board of Health and Welfare* (*Socialstyrelsen*). Specifically, the data has been extracted from the [Statistikdatabas för läkemedel](https://sdb.socialstyrelsen.se/if_lak/val.aspx) where data about all medications that have been bought/given based on a prescription in Sweden since 2006 are available.

Here is the file structure for the app:

```bash
..
└── app/
│   ├── app.R
│   └── socialstyrelsen_2022-02-18.csv
```
Docker images are built from sets of instructions given in a so-called Dockerfile. Create a file called Dockerfile (the name of the file should be exactly 'Dockerfile' and it should not have any file extension) using any text editor you have and insert the code below or simply download this example. Place this file in the parent folder of the folder `app`, so inside the `shiny-adhd-medication-sweden` folder.

```bash
FROM rocker/shiny:4.2.0

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git libxml2-dev libmagick++-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Command to install standard R packages from CRAN; enter the list of required packages for your app here
RUN Rscript -e 'install.packages(c("shiny","tidyverse","BiocManager"), dependencies = TRUE)'

# Command to install packages from Bioconductor; enter the list of required Bioconductor packages for your app here
RUN Rscript -e 'BiocManager::install(c("Biostrings"),ask = F)'

RUN rm -rf /srv/shiny-server/*
COPY /app/ /srv/shiny-server/

USER shiny

EXPOSE 3838

CMD ["/usr/bin/shiny-server"]
```
Here is what your file structure should look like after you create the new files.

```bash
..
├── app/
│   ├── app.R
│   └── socialstyrelsen_2022-02-18.csv
└── Dockerfile
```

In this example two packages were installed from the standard R packages: `shiny` and `tidyverse`. This was done in the line `RUN Rscript -e 'install.packages(c("shiny","tidyverse"))'`. In addition, one package was installed from `Bioconductor` - `Biostrings`. This was done in the line `RUN Rscript -e 'BiocManager::install(c("Biostrings"),ask = F)'`. If you are building your own app instead of this example app, you can add your own packages here as needed by your app.

The folder app and its contents are copied into the image in the line `COPY /app/* /srv/shiny-server/`. If you are building your own app and you use a different folder name, change the folder names in this line and lines below. If some of the dependecies of the app are located in different folders, these other folders should be copied into the image separately.

You can see our example app with these files in this <a href="https://github.com/ScilifelabDataCentre/shiny-adhd-medication-sweden" target="_blank">GitHub</a> repository.

### Build your Docker image
Ensure that Docker Desktop is running. Open Terminal (or Windows Terminal) and navigate to the folder where your app files and the Dockerfile are located.
```bash
cd path/to/your/folder
```

Run the Docker command to build your image as shown below. Replace <your-image-name> with your own image name. Note that the dot at the end of the command is important. Please note that building the image may take a while.

!!! warning  "Note"
    The dot **(.)** at the end of the command is important. This sets the build context to the current directory. This means that the build expects to find the Dockerfile in the directory where the command is invoked

```bash
docker build --platform linux/amd64 -t <your-image-name>:<your-image-tag> .
```
Once the process is complete, your newly created image should appear on Docker Desktop under the Images. Alternatively, run the following command in the Terminal to inspect images on your computer. You should see your image in the list.
```bash
docker images
```
In order to test that the image you just built works you need to run a container from this image. To do that, run the following command in the Terminal.
```bash
docker run --rm -p <local-port>:<container-port> <your-image-name>:<your-image-tag>
```

If everything went as it should, you should now be able to navigate to `http://localhost:<local-port>` in your browser and see and interact with your Shiny app.

??? "Click to see exact commands"
    Run the following command to build the docker container
    !!! warning  "Note"
        The dot **(.)** at the end of the command is important. This sets the build context to the current directory. This means that the build expects to find the Dockerfile in the directory where the command is invoked
    ```bash
    docker build --platform linux/amd64 -t adhd-shiny-app .
    ```
    !!! tip "Pro tip"
        It is a good idea to use your Dockerhub username when building and tagging images as this makes it possible to push images to an image registry such as Dockerhub.
        Using versioning is very helpful as well.
        As an example, the command above could be written as:
        ```
        docker build --platform linux/amd64 -t <your-dockerhub-username>/adhd-shiny-app:v1.0.0 .
        ```
    After building the image you can then run it with the following command

    ```bash
    docker run -p 3838:3838 <your-dockerhub-username>/adhd-shiny-app
    ```

    Once it is running you should see that it is available under <a href="http://localhost:3838" target="_blank">http://localhost:3838</a> (or see what the container tells you in the terminal window, it should say "Starting listener on: ..."). Navigate to this link in your browser and try out the app.

    !!! tip "Pro tip"
        It is often useful to run the container in detached mode so that it can run in the background.
        As an example, the command above could be written as:
        ```bash
        docker run -d -p 3838:3838 <your-dockerhub-username>/adhd-shiny-app
        ```

### Publish your Docker Image

Once the image is built and visible on Docker Desktop, pick *"Push to Hub"* among the options for your app image. Alternatively, you can also use the following command from the terminal instead

```bash
docker push <your-dockerhub-username>/<some-name>:<some-tag>
```

Keep in mind the you might need to login to you DockerHub user in case you haven't done so already. This can be done as follows:

```bash
docker login
```

This should publish your image on `https://hub.docker.com/r/<your-dockerhub-username>/<some-name>`. For example, our example app image for the flask web app is available at `scilifelabdatacentre/workshop-flask-web-app`. Please note, if you create an image to publish on Scilifelab Serve, your image should stay available even after your app is published on Serve because it will be fetched with regular intervals.

## Step 3. Hosting your application on SciLifeLab Serve

### Create a user account on SciLifeLab Serve

If you do not already have a user account on SciLifeLab Serve, [create an account](https://serve.scilifelab.se/signup/).

### Create a project

Every app and model has to be located within a project. Projects that you have created/been granted access to can be found under **[My projects](https://serve.scilifelab.se/projects/)** page.

You need to be logged in to create a project. To create a project, click on the corresponding button on that page. Choose blank/default project if asked. The name and description of the project are visible only to you and those who you grant access to the project. Once the project is created, you will be taken to the project dashboard where you can create different types of apps.

### Create an app

In order to host an app that we just built click the Create button on the Shiny app card. Then enter the following information in the form:

* **Name:** Name of the app that will be displayed on the Public apps page.
* **Description:** Provide a description of the app, will also be displayed on the Public apps page. This functions as an abstract describing your application.
* **Subdomain:** This is the subdomain that the deployed app will be available at (e.g., a subdomain of 'my-cool-app' would mean that the app will be available at my-cool-app.serve.scilifelab.se). If no subdomain name is entered, a random name will be generated by default. By typing in the input box you can specify the custom subdomain name of your choice.
* **Permissions:** The permissions for the project. There are four levels of permissions for an app:
    - **Private:** The app can only be accessed by the user that created the app (sign in required). Please note that we only allow the permissions to be set to Private temporarily, while you are developing the app. Eventually each app should be published publicly.
    - **Project:** All members of the project where the app is located will be able to access the app (sign in required). Please note that we only allow the permissions to be set to Project temporarily, while you are developing the app. Eventually each app should be published publicly.
    - **Link:** Anyone with the URL can access the app but this URL will not be publicly listed anywhere by us (this option is best in case you want to share the app with certain people but not with everyone yet).
    - **Public:** Anyone with the URL can access the app and the app will be displayed under Public apps page.
* **Hardware:** Amount of CPU and RAM dedicated to your app. By default there is only one option that is sufficient for most users; get in touch with us if your app needs more hardware resources.
* **Port:** The port that the Shiny server runs on (usually 3838). Note that we only allow ports in the range 3000-9999.
* **Image:** Your username, image name and tag on DockerHub (your-dockerhub-username/your-image-name:your-image-tag) or full url to the image on a different repository. Note that each version of your app should have a unique tag. Once an image with a certain tag has been deployed once it will no longer be possible to change this version without a new tag.

You can leave the other fields as default.

Press the Submit button to create the app. It may take 3-5 minutes for your app to start.

## Congratulations!

Congratulations, you just built a docker image, pushed it to Dockerhub and started hosting your first app on Scilifelab Serve!

Feel free to get in touch with the SciLifeLab Serve team with questions: serve@scilifelab.se.
