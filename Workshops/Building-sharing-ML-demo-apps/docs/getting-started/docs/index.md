---
hide:
  - navigation
---
# Building and sharing AI applications within ecology and biodiversity

During the tutorial we will start from a trained model and demonstrate step by step how you can create a graphical user interface for your application, prepare it for deployment, and make it available on the web with a URL. To get started make sure the following tools are available on your machine.


## Downloading Docker or Docker Desktop

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

## Create an account on Dockerhub and Sign In

As part of this workshop, you will create a Docker Image and push to it Docker's Image Regsitry called Dockerhub. To do this, you need to create a docker account, which you can do by going to their <a href="https://hub.docker.com/" target="_blank">website</a> and creating an account. Once this is done, you can go to the terminal on your computer and run the following command:

```console
docker login
```

## Workshop Preparation

In order to follow this workshop, make sure that you are running Python 3.10 or later. Run this command in your Terminal to find out.

```console
python --version
```

Then, you need to download the files for this workshop to your computer. If you have git, you can simply git clone this repository.

```console
git clone https://github.com/ScilifelabDataCentre/serve-tutorials
```

Otherwise [press this link to download a .ZIP archive](https://github.com/ScilifelabDataCentre/serve-tutorials/archive/refs/heads/main.zip) and unzip it manually.

Finally, in your Terminal, navigate to the folder of this particular tutorial and create a Python virtual environment where you can install gradio.

```console
cd serve-tutorials/Workshops/Building-sharing-ML-demo-apps/
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install gradio
```

Once all of these tools are installed and running, you can move onto the hands-on part by [clicking here](https://sbdi-hands-on.serve.scilifelab.se/)