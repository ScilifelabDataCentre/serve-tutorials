---
hide:
  - navigation
---
# Packaging and sharing data science applications as docker container images

This workshop will introduce Docker containers and how you can use them to package applications. By the end of this workshop, we hope you will know how to use Docker on your local machine, package applications with their dependencies, upload the packaged apps to Dockerhub as images. During the workshop we will start with a short talk introducing containers and docker. We will go over the basic commands that you can use to build and run docker containers and expose ports to your local machine.
The we will show an example of a shiny application, prepare it for deployment by packaging it as a docker container and make it available on the web with a URL. The target audience of this tutorial are researchers who build applications and tools from different frameworks and want to know about packaging them.

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


## Step 1. Building a basic image and publishing to dockerhub

In this section we will go through some basic docker commands, build a docker image and then publish it to dockerhub.

### Basic Docker commands

You have already seen alot of these commands but just to refresh here are a few docker commands

#### Starting and Stopping

* [`docker start`](https://docs.docker.com/engine/reference/commandline/start) starts a container so it is running.
* [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop) stops a running container.
* [`docker restart`](https://docs.docker.com/engine/reference/commandline/restart) stops and starts a container.

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

### Build a Docker image

Ensure that Docker Desktop is running. Open Terminal (or Windows Terminal) and navigate to the folder where your app files and the Dockerfile are located.

```bash
cd path/to/your/folder
```

Run the Docker command to build your image as shown below. Note that the dot at the end of the command is important. Please note that building the image may take a while.

```bash
docker build -t <some-name>:<some-tag> .
```
Replace `<some-name>:<some-tag>` with the name of the app and some tag to identify this particular version. For instance `my-web-app:v2`. 
Once the process is complete, run the following command in the Terminal. You should see your image in the list.

```bash
docker image ls
```

In order to test that the image you just built works you need to run a container from this image. To do that, run the following command in the Terminal.

```bash
docker run --rm -it -p <local-port>:<container-port> <some-name>:<some-tag>
```

If everything went well, you should now be able to navigate to `http://localhost:<local-port>` in your browser and see and interact with your app.


### Basic Python app

We start with the basic python flask app. Flask is a lightweight and flexible framework for web development and web applications based on Python. To create this application we will have to create the following files with the following file structure

```bash
..
├── requirements.txt
├── app.py
└── Dockerfile
```

Create a directory named `flask-web-app`
```bash
mkdir flask-web-app
```
Then create the files mentioned above. The files will look as follows
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

Once all of these files are created, run the following command to build a docker container
```bash
docker build -t flask-web-app .
```
!!! info "Pro tip"
    It is a good idea to use your repository name when building and tagging images as this makes it possible to push to your repository.
    Using versioning is very helpful as well.
    As an example, the command above could be written as:
    ```
    docker build -t <your-dockerhub-repository>/flask-web-app:v1.0.0 .
    ```
After building the image you can then run it with the following command

```bash
docker run -p 5000:5000 flask-web-app
```

Once it is running you should see that it is available under <a href="http://localhost:5000" target="_blank">http://localhost:5000</a> (or see what Flask tells you in the terminal window, it should say "Running on URL: ..."). Navigate to this link in your browser and try out the app.

!!! info "Pro tip"
    It is often useful to run the container in detached mode so that it can run in the background.
    As an example, the command above could be written as:
    ```
    docker run -d -p 5000:5000 flask-web-app
    ```

### Publish your Docker image

You have now built and tested an image for your app on your computer. In order to be able to host this image on SciLifeLab Serve it needs to be published in a so-called image registry. Below, we show how to publish your image on [DockerHub](https://hub.docker.com) as an example but you can choose any public image registry (for example, on GitHub).

Register on [DockerHub](https://hub.docker.com/) and sign in with your account on Docker Desktop app.

Next, re-build your image as described above, this time including your DockerHub username in the image name, as shown below. 

```bash
docker build -t <your-dockerhub-username>/<some-name>:<some-tag> .
```

Once the image is built and visible on Docker Desktop, pick *"Push to Hub"* among the options for your app image. Alternatively, you can also use the following command from the terminal instead

```bash
docker push <your-dockerhub-username>/<some-name>:<some-tag>
```

Keep in mind the you might need to login to you DockerHub user in case you haven't done so already. This can be done as follows:

```bash
docker login --username=<your-dockerhub-username>
```

This should publish your image on `https://hub.docker.com/r/&lt;your-dockerhub-username&gt;/&lt;some-name&gt;:&lt;some-tag&gt;`. For example, our example app image for the flower image classification app is available on `hamzaisaeed/gradio-workshop:flower_classification`. Please note that your image should stay available even after your app is published on Serve because it will be fetched with regular intervals.

## Step 3. Hosting your application on SciLifeLab Serve

### Create a user account on SciLifeLab Serve

If you do not already have a user account on SciLifeLab Serve, [create an account](https://serve.scilifelab.se/signup/).

### Create a project

Every app and model has to be located within a project. Projects that you have created/been granted access to can be found under **[My projects](https://serve.scilifelab.se/projects/)** page.

You need to be logged in to create a project. To create a project, click on the corresponding button on that page. Choose blank/default project if asked. The name and description of the project are visible only to you and those who you grant access to the project. Once the project is created, you will be taken to the project dashboard where you can create different types of apps.

### Create an app

In order to host an app that we just built click the Create button on the Custom app card. Then enter the following information in the form:

* **Name:** Name of the app that will be displayed on the Public apps page.
* **Description:** Provide a brief description of the app, will also be displayed on the Public apps page.
* **Subdomain:** This is the subdomain that the deployed app will be available at (e.g., a subdomain of r46b61563 would mean that the app would be available at r46b61563.serve.scilifelab.se). If no subdomain name is entered, a random name will be generated by default. By clicking on New you can specify the custom subdomain name of your choice (provided that it is not already taken). This subdomain will then appear in the Subdomain options and the subdomain will appear in the format 'name-you-chose.serve.scilifelab.se'.
* **Permissions:** The permissions for the app. There are 3 levels of permissions you can choose from:
  - **Private:** The app can only be accessed by the user that created the app (sign in required). Please note that we only allow the permissions to be set to Private temporarily, while you are developing the app. Eventually each app should be published publicly.
  - **Project:** All members of the project where the app is located will be able to access the app (sign in required). Please note that we only allow the permissions to be set to Project temporarily, while you are developing the app. Eventually each app should be published publicly.
  - **Public:** Anyone with the URL can access the app and the app will be displayed under Public apps page.
* **App Port:** The port that the your app runs on (in case of our template it will be `7860`).
* **DockerHub Image:** Name of the image on DockerHub or full URL to the image on a different repository.

You can leave the other fields as default.

## Congratulations!

Congratulations, you just built and started hosting your first machine learning demo application!

Feel free to get in touch with the SciLifeLab Serve team with questions: serve@scilifelab.se.
