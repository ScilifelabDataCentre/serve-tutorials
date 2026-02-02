---
hide:
  - navigation
---
# Public hosting of Shiny apps: hands-on exercise

This tutorial will guide you through packaging an example Shiny application as a Docker image, uploading this packaged Docker image to DockerHub, and, subsequently, making it available as a web application with a publicly accessible URL. The target audience of this tutorial is researchers who are comfortable working with R code and build Shiny applications. Familiarity with working with terminal is useful but not necessary.

Throughout this tutorial, we will use our example Shiny application that you can download. If you have your own Shiny application that you would like to package and make available, feel free to use that one instead of our example application. You will be able to follow the steps outlined below but simply use your own version of R, packages, files, data, etc.

## Part 1. Install Docker Desktop and sign in

In this tutorial, we will be using Docker Desktop. Docker Desktop is the all-in-one package to build Docker images and run applications from DOcker images (referred to as *running a container*). Follow the steps below to install it if you do not already have it on your computer.

### Steps to Install Docker Desktop

1. **Download Docker Desktop Installer**  
Visit the Docker Desktop <a href="https://www.docker.com/products/docker-desktop/" target="_blank">download page</a> and download the installer for your operating system.

2. **Run the Installer**  

3. **Follow the Installation Wizard**  
Follow the on-screen instructions to complete the installation.

4. **Start Docker Desktop**  
Once the installation is complete, Docker Desktop will start automatically.You can also start it manually.

5. **Verify installation**  
Open a terminal (Windows Terminal, Command Prompt, PowerShell, or any other terminal) and run the following command to verify the installation:

 ```sh
 docker --version
 ```

You should see the Docker version information displayed.

6. **Run a test container**  
To ensure Docker is working correctly, run a test container:

 ```sh
 docker run hello-world
 ```

This command downloads a test image and runs it in a container. If successful, you will see a message indicating that Docker is installed correctly.

### Create an account on Dockerhub and sign In

You will also you need to have a DockerHub account. You can create an account by going to their <a href="https://hub.docker.com/" target="_blank">website</a>. Once this is done, you can open Docker Desktop and sign in (you will find the option to sign in in the top right corner). Alternatively, you can go to the terminal and run the following command:

```console
docker login
```

## Part 2. Download and run our example Shiny app on your computer

We prepared an example Shiny application that you can work with today. Please download these files, place them in a single folder called `app`, and make sure you can run the Shiny application on your computer (for example, using RStudio interface) without issues:

- `app.R`: [TO-DO: ADD URL]
- `population_by_municipality.csv`: [TO-DO: ADD URL]

Here is the file structure for the app so far:

```bash
..
└── app/
│   ├── app.R
│   └── population_by_municipality.csv
```

This application was built with R version *4.4.1* but we expect it to run without issues with later versions as well. It assumes that there is a number of packages in the R environment, install them if you do not already have them.

Those who wish to use their own Shiny app do not need to download our example but should also place all files that your app needs to run into a single folder called `app`.

## Part 3. Build a Docker image with the app and publish to Dockerhub

*Docker image* is essentially as a packaged archive that contains everything that your application needs (including the operating system, R, any packages, any files needed). The advantage of packaging applications as Docker images is that are portable - they that can be easily launched from any computer or server without the need to configure a similar or identical environment.

### Prepare a Dockerfile

Docker images are built from sets of instructions given in a so-called *Dockerfile*. Create a file called `Dockerfile` (the name of the file should be exactly 'Dockerfile' and it should not have any file extension) using any text editor you have and insert the code below. Place this file in the parent folder of the folder `app`.

```bash
# Base image where the R version is specified
FROM rocker/shiny:4.4.1

# Install the required R packages. They all need to be listed here.
RUN Rscript -e 'install.packages(c("dplyr", "ggplot2", "scales", "readr"), dependencies = TRUE)'

# Copy the app files (scripts, data, etc.)
RUN rm -rf /srv/shiny-server/*
COPY /app/ /srv/shiny-server/

# Ensure that the expected default user is present in the container (this command needs to be here for later steps)
RUN if id shiny &>/dev/null && [ "$(id -u shiny)" -ne 999 ]; then \
        userdel -r shiny; \
        id -u 999 &>/dev/null && userdel -r "$(id -un 999)"; \
    fi; \
    useradd -u 999 -m -s /bin/bash shiny; \
    chown -R shiny:shiny /srv/shiny-server/ /var/lib/shiny-server/ /var/log/shiny-server/

# Other settings
USER shiny
EXPOSE 3838

CMD ["/usr/bin/shiny-server"]
```

Here is what your file structure should look like after you create the Dockerfile.

```bash
..
├── app/
│   ├── app.R
│   └── population_by_municipality.csv
└── Dockerfile
```

Let us look a little bit at what instructions the Dockerfile contains. The first step is to take a specific version of R, we specified *4.4.1*. After that, the packages are installed by using the R `install.packages()` command where we listed all required packages. In the next step is to copy the relevant app files (the R file and the data) into a specific location in the Docker image: `COPY /app/* /srv/shiny-server/`. Finally, the line `EXPOSE 3838` instructs that the port 3838 should be made available (this information will be used later).

If you are building this image for your own app you should specify your own version of R, list of packages, folder name(s). If some of the dependecies of the app are located in different folders, these other folders should be inside the `app` folder.

!!! warning  "Note"
    There are two things that we simplified in the Dockerfile above to make sure the Docker image is built fast during the tutorial session. One is that we skipped the step of updating the operating system. This should preferably be done as the second step, immediately after downloading the base image. 
    
    In addition, it is better to capture the exact R environment that is used for this application (specifically, which R packages were used and which versions) so that we can reproduce it in the Docker image of the application exactly (instead of manually installing packages as we did in thi example). The best way to achieve this is by using the [*renv*](https://rstudio.github.io/renv/index.html) package to create a snapshot and then restore this snapshot as one of the steps in the Dockerfile instructions. 
    
    You can find an an example of how to do both of these [in our detailed tutorial](https://serve.scilifelab.se/docs/application-hosting/shiny/) which we recommend reading before you start long-term hosting of a Shiny application.


### Build your Docker image

Ensure that Docker Desktop is running. Open a terminal window (Windows Terminal, Command Prompt, PowerShell, or any other terminal) and navigate to the folder where your app files and the Dockerfile are located.

```bash
cd path/to/your/folder
```

Run the Docker command to build your image as shown below. Replace <your-image-name> with your own image name, it can be anything you wish. Note that the dot at the end of the command is important. Please note that building the image may take a while.

!!! warning  "Note"
    The dot **(.)** at the end of the command is important. This sets the build context to the current directory. This means that the build expects to find the Dockerfile in the directory where the command is invoked

```bash
docker build --platform linux/amd64 -t <your-image-name> .
```

Once the process is complete, your newly created image should appear on Docker Desktop under the Images menu. Alternatively, run the following command in the terminal to inspect images on your computer. You should see your image in the list.

```bash
docker images
```

To test that the image you just built works, you need to launch your app from this image. To do that, run the following command in the terminal.

```bash
docker run --rm -p 3838:3838 <your-image-name>
```

If everything went as it should, you should see a confirmation that your app is running and you should be able to navigate to `http://localhost:3838` in your web browser and interact with your Shiny app.

### Share your Docker Image

In order to share your Docker image and use it outside of your own computer, you need to upload it to a so-called *container registry*. In this tutorial, we will upload the image to [DockerHub](https://hub.docker.com) but any other registry can be used.

First, you need to rename the image to add your DockerHub username to the beginning of the name. You also need add a *tag*. A *tag* is simply the version; you can use *1*, *v1*, the date, etc.. For each subsequent version, you will be changing the tag only so that you can distinguish between different images and different versions of the same image. Copy the command below but replace the relevant parts.

```bash
docker image tag <your-image-name> <your-dockerhub-username>/<your-image-name>:<your-tag>
```

You should now see two copies of your image with different names and tags. In Docker Desktop, among the options for the one with your DockerHub username pick *"Push to Hub"* which will upload it to DockerHub. Alternatively, you can also use the following command from the terminal instead.

```bash
docker push <your-dockerhub-username>/<your-image-name>:<your-tag>
```

Your image should now be listed on this page: *https://hub.docker.com/r/your-dockerhub-username/your-image-name*. We also created a Docker image for our example app, and it is listed here: https://hub.docker.com/r/ 

[TO-DO: ADD URL HERE].

!!! warning  "Note"
    Container registry is a catalogue of public and private images that can be downloaded (*pulled*). There are many big and small container registries. The most popular ones are [DockerHub](https://hub.docker.com) and [GHCR (GitHub Container Registry)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry). Both of these are run commercial companies that offer a free tier that is sufficient for us. We will use DockerHub as our registry of choice because it is the one that is integrated with Docker Desktop.

    You can also automate building and publishing your image by having your application code and files in a GitHub repository and setting up a corresponding GitHub Action. This is most useful in cases where you plan to make changes to your Shiny app often or in cases when build an image on your own computer takes a long time. Using GitHub actions to build and publish a Docker image is covered in our [detailed guide on Shiny apps](https://serve.scilifelab.se/docs/application-hosting/shiny/).

## Part 4. Make the app available with a URL

In this part we will go through the process of adding a Shiny application to [SciLifeLab Serve](https://serve.scilifelab.se/). SciLifeLab Serve is a national platform developed and maintained by SciLifeLab. It is available free of charge to all life science researchers at Swedish research institutes. If you wish to use another hosting option (for example, use a paid public cloud platform), the same Docker image can be used but you will need to follow the instructions of the corresponding platform.

### Create a user account on SciLifeLab Serve

If you do not already have a user account on SciLifeLab Serve, [create an account](https://serve.scilifelab.se/signup/).

### Create a project

Every app has to be located within a project. Projects that you have created/been granted access to can be found under **[My projects](https://serve.scilifelab.se/projects/)** page.

You need to be logged in to create a project. The name and description of the project are visible only to you and those who you grant access to the project. Once the project is created, you will be taken to the project dashboard where you can create different types of apps.

### Create an app

In order to host an app that we just built, click the *Create* under the Shiny app option. Enter the following information in the form. Leave the fields not mentioned here with default choices; they are useful for specific cases described in the detailed user guide.

* **Subdomain:** Custom subdomain of your choice. This is the subdomain that the deployed app will be available at (e.g., a subdomain of 'my-cool-app' would mean that the app will be available at my-cool-app.serve.scilifelab.se). If no subdomain name is entered, a random name will be generated by default. 
* **Port:** The port that the Shiny server runs on. In our case, we chose *3838*.
* **Image:** In our case, it should be: `your-dockerhub-username/your-image-name:your-image-tag`. Note that each version of your app in the future should have a unique tag.
* **Name:** Name of the app.
* **Description:** Provide a description of the app.
* **Permissions:** The permissions for the project. In our case, we will choose *Link*. Here is what all the options mean:
    - **Private:** The app can only be accessed by the user that created the app (sign in required). Please note that we only allow the permissions to be set to Private temporarily, while you are developing the app. Eventually each app should be published publicly.
    - **Project:** All members of the project where the app is located will be able to access the app (sign in required). Please note that we only allow the permissions to be set to Project temporarily, while you are developing the app. Eventually each app should be published publicly.
    - **Link:** Anyone with the URL can access the app but this URL will not be publicly listed anywhere by us (this option is best in case you want to share the app with certain people but not with everyone yet).
    - **Public:** Anyone with the URL can access the app and the app will be displayed under Public apps page.

Press the **Submit** button to create the app. It should take about 5 minutes for your app to start (note that it will have the status *Running* before it is completely loaded). Once the app is available on the subdomain you chose, anyone with the link will be able to access and interact with the app on that URL (if you chose the "Link" permission level).

## Congratulations!

Congratulations, you just started hosting your first application! With this knowledge, you can now go back and try a different application or learn more about specific options when building a Docker image or launching an application on SciLifeLab Serve.

Feel free to get in touch with the SciLifeLab Serve team with questions: serve@scilifelab.se.

!!! warning  "Note"
    This tutorial focused on hosting Shiny applications on a web server with a URL. But Docker images are powerful because can be used in other ways too. When a Docker image that you created is uploaded to DockerHub or another container registry, anyone can download and run it on their computer. This means that you do not have to have a public URL but can instead share the Docker image with, for example, colleagues or readers of your scientific article by simply providing the image URL. 
    
    The app user does not need to have R, any packages, or any files. They just need to have Docker running on their computer.

    First, the user can download ("pull") the image to their computer:

    ```bash
    docker pull <your-dockerhub-username>/<your-image-name>:<your-tag>
    ```

    Then, the user can run the app and interact with it at `http://localhost:3838` in their web browser.

    ```bash
    docker run --rm -p 3838:3838 <your-dockerhub-username>/<your-image-name>:<your-image-tag>
    ```