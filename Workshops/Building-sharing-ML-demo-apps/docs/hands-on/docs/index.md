---
hide:
  - navigation
---
# Building and sharing AI applications within ecology and biodiversity

During the tutorial we will start from a trained model and demonstrate step by step how you can create a graphical user interface for your application, prepare it for deployment, and make it available on the web with a URL. The target audience of this tutorial are researchers working with machine learning models that do not have web development background but still want to share demos of their models as web applications. We will demonstrate the use of specific tools which make this process easy.

Note that the setup described here will cover the needs of a large majority of researchers when they want to share their ML model, allowing to give the app users instant predictions and good performance overall. In the minority of cases performance might be an issue when using this approach - perhaps your model is really large and needs a lot of time or resources to make predictions or you care about fast inference down to milliseconds. In these latter cases there are more specialized ways to build or serve applications, those cases are not covered here.

## Step 0. Setup (Skip if you followed setup instructions)

### Downloading Docker or Docker Desktop

Docker Desktop is the all-in-one package to build images and run containers.

#### Steps to Install Docker Desktop

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

#### Create an account on Dockerhub and Sign In

As part of this workshop, you will create a Docker Image and push to it Docker's Image Regsitry called Dockerhub. To do this, you need to create a docker account, which you can do by going to their <a href="https://hub.docker.com/" target="_blank">website</a> and creating an account. Once this is done, you can go to the terminal on your computer and run the following command:

```console
docker login
```

You should see something like

```console {: .optional-language-as-class .no-copy}
Authenticating with existing credentials... [Username: your-usernname]

i Info → To login with a different account, run 'docker logout' followed by 'docker login'


Login Succeeded

```

You are now ready to start with the workshop hands-on.

## Step 1. Building a user interface

There are multiple frameworks that simplify the process of building apps with graphical user interfaces for machine learning models. For example, [Gradio](https://github.com/gradio-app/gradio) and [Streamlit](https://github.com/streamlit/streamlit) are such open source frameworks with a good community around them. In this tutorial we make use of Gradio. Here we will only cover basic functionality of Gradio which should suffice for most of the needs of researchers in life sciences. We want to note that Gradio (as well as Streamlit) offers niche functionality and flexibility for specific use cases so be sure to check [the official documentation](https://www.gradio.app/docs/) once you learn the basics here.

In this tutorial we use examples from the official [Gradio documentation](https://www.gradio.app/guides/quickstart) as well as custom examples that we created ourselves.

### Preparation

First, you need to download the files from this tutorial to your computer. If you have `git`, you can simply `git clone` this repository. Otherwise [press this link to download a .ZIP archive](https://github.com/ScilifelabDataCentre/serve-tutorials/archive/refs/heads/main.zip) and unzip it manually.

```bash
git clone https://github.com/ScilifelabDataCentre/serve-tutorials
```

In order to follow this tutorial, make sure that you are running Python 3.10 or later. Run this command in your Terminal to find out.

```bash
python --version
```
Finally, in your Terminal, navigate to the folder of this particular tutorial and create a Python virtual environment where you can install gradio.

```bash
cd serve-tutorials/Workshops/Building-sharing-ML-demo-apps/
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install gradio
```

If all is successful, you are now ready to start looking at the examples in the `example_apps/` folder and trying out different things in the templates that we prepared.

### Simplest application with Gradio

We start with the basic case where the user provides custom input in a text field and receives output in text format. This example is in the `example_apps/hello_app.py` file. Let's first run it and see what it gives us. To run this and all the subsequent apps in this tutorial you can enter the following in the terminal:

```bash
gradio example_apps/hello_app.py
```

Once it is running you should see that it is available under http://localhost:7860 (or see what Gradio tells you in the terminal window, it should say "Running on local URL: ..."). Navigate to this link in your browser and try out the app.

Let's take a closer look at what the code in this file does.

```python
import gradio as gr

def greet(name):
   return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch(server_name="0.0.0.0", server_port=7860)
```

We start by importing the *Gradio* package. We define the function that Gradio will use. This simple function takes one input and returns one output.

Using the `Interface` class we define what the app should look like. We pass the following parameters: `fn` specifies the function that the app should be running, `inputs` specifies what fields the user should be allowed to give as input, `output` specifies what kind of output the function will be showing the user.

Finally, the launch method instructs to launch the defined app. By default your app will run on port 7860 (can be changed if you wish).

This example demonstrates the three basic components that your app will need - the function that the app will be based on, the interface definition, and the launch command. We will now build on this simplest case to add more complex scenarios and customize the app.

Lets move onto the task for the workshop

### Build a Gradio app for a trained model

In this step, you will build a Gradio web application around a **pre-trained flower classification model**.

#### Flowers Classification Model

Information about how this model was trained can be found [here](https://github.com/ScilifelabDataCentre/serve-tutorials/tree/main/Webinars/2023-Using-containers-on-Berzelius/flowers-classification). You can follow the instructions to train the model your self but keep in mind it takes quite a while (~ 4 hours) with limited CPUs. For information about the dataset used, [see](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/).

The goal is to take an existing PyTorch model, wrap it in a Gradio interface, and customize the app to make it user-friendly and visually appealing.

An example application structure is provided in the `hands_on_app/` folder. You will extend this example by adding your own Gradio app code.

---

### 1. Explore the provided folder structure

Navigate to the `hands_on_app/` directory using the following command

```bash
cd hands_on_app
```

You should see a structure (you can check this with ```tree``` or ```ls``` command ) similar to this:

```
hands_on_app/
├── requirements.txt
├── main.py
├── data/
└── ...
```

- `requirements.txt` lists the Python packages required to run the app.
- `main.py` is where you will write your Gradio application.
- `data/` will contain the trained model and label files used by the app.

---

### 2. Install required Python packages

Before running or modifying the app, install the required dependencies.

From inside the  `hands_on_app` folder, run:

```
pip install -r requirements.txt
```

This will install all the dependencies for you.

---

### 3. Download and add the trained model

The app expects a trained PyTorch model to be available locally.


To do this, you need to download the flower classification model (`flower_model_vgg19.pth`) to the `data` directory.

The app is configured to use the model from the `data` directory. So you need to go into the directory using

```bash
cd data
```

and then run the following command to download the model

```bash
curl -O -J https://nextcloud.dc.scilifelab.se/s/GSf2g5CAFxBPtMN/download
```
You can also manually download the model by [clicking here](https://nextcloud.dc.scilifelab.se/s/GSf2g5CAFxBPtMN/download) and then manually moving the model into the data folder.

---

### 4. Implement the Gradio app in `main.py`

Open `main.py`. This file looks as follows:

```python
import gradio as gr
import torch
from PIL import Image
from torchvision import transforms
import torchvision.models as models

# Before you start, download and place the trained model to the data folder, it should be available at 'data/flower_model_vgg19.pth'
# https://nextcloud.dc.scilifelab.se/s/GSf2g5CAFxBPtMN/download

model = torch.load('data/flower_model_vgg19.pth')
model.eval()
# Download human-readable labels for ImageNet.
with open('data/flower_dataset_labels.txt', 'r') as f:
    labels=f.readlines()

def predict(inp):
  inp = transforms.ToTensor()(inp).unsqueeze(0)
  with torch.no_grad():
    prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)
    confidences = {labels[i]: float(prediction[i]) for i in range(102)}
  return confidences

```

The file does the following at the moment

- Loads the trained PyTorch model  
- Preprocesses user-uploaded images  
- Runs inference using the model

At a minimum, your app should include:

- A **prediction function** that takes an image as input and returns model predictions (this is already implemented)
- A **Gradio interface definition** (`gr.Interface`)
- A **launch command** to start the app

You now need to add the interface definition and the launch command.

To implement the interface definition add the following line to your code

```python
interface = gr.Interface(fn=predict, inputs=gr.Image(type="pil"), outputs=gr.Label(num_top_classes=3))
```

Finally, add the launch command to your code

```python
interface.launch(server_name="0.0.0.0", server_port=7860)
``` 


Once implemented, you should be able to start your app by running:

```
python main.py
```

If everything works correctly, Gradio will print a message similar to:

```
Running on local URL: http://localhost:7860
```

Open this URL in your browser and try uploading an image to test your app.

### What you should have at the end

By the end of this step, you should have:

- A working Gradio app that wraps a trained image classification model
- A clear understanding of how model inference is connected to a web interface
- An app that is ready to be packaged and deployed in the next steps of the workshop

---

### (Optional) Customize your application

If you have already completed the steps to create the image classification app here are some additional things you can look at to add to the app and customize it:

- Improve the **layout**
- Add a **title and description** to explain what the model does
- Show the **top-N predictions** instead of three
- Display **confidence scores**
- Add example images users can try
- Customize colors, labels, and text to improve usability

This is your chance to experiment and be creative — there is no single “correct” solution.

In the following section, we will package this application as a Docker image and deploy it.

---



## Step 2. Packaging your application as a docker image and hosting it on SciLifeLab Serve

There are multiple ways to host your application on a web server. Below, we demonstrate how to host on SciLifeLab Serve, a dedicated machine learning model and app hosting platform for life science researchers in Sweden that is free. To host your app on SciLifeLab Serve, you first need to package it as a Docker image. This is a simple process even if you have not done this before so do not worry. You can simply follow the steps below.

You will need to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your computer to be able to build an image.

### Create a Dockerfile

Now you are ready to create a Dockerfile. Dockerfile is a file containing instructions for how your Docker image should be built. See [the official documentation]((https://docs.docker.com/engine/reference/builder/)) if you are curious to learn more, but for the purpose of hosting your app it is sufficient to simply copy and if needed adjust the template below. 

First, create a file called simply `Dockerfile`, without any file extension. Then copy the following content into the file

```dockerfile
# Select base image (can be ubuntu, python, shiny etc)
FROM python:3.11-slim

# Create user name and home directory variables. 
# The variables are later used as $USER and $HOME. 
ENV USER=username
ENV HOME=/home/$USER

# Add user to system
RUN useradd -m -u 1000 $USER

# Set working directory (this is where the code should go)
WORKDIR $HOME/app

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy code and start script (this will place the files in home/username/)
COPY requirements.txt $HOME/app/requirements.txt
COPY main.py $HOME/app/main.py
# copy any other files that are needed for your app with the directory structure as your files expect
COPY data/ $HOME/app/data

RUN pip install --no-cache-dir -r requirements.txt \
    && chown -R $USER:$USER $HOME \
    && rm -rf /var/lib/apt/lists/*

USER $USER

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "main.py"]

```

This Dockerfile instructs to start with a base image containing Python version 3.11 (it is going to contain Ubuntu as operating system and components required to run Python), install the required packages listed in `requirements.txt`, copy all the scripts and other necessary files for the app into the image (copy your own files here as well), and, finally, points to the script to start the app. The Dockerfile also contains information about which user should be running the app and which port it should expose.

At this point, you should have the following file structure in your app directory:

```bash
..
├── requirements.txt
├── main.py
├── data   
    └── ... (model and any other static files required)
├── ... (any other files your app requires)
└── Dockerfile
```

### Build a Docker image

Ensure that Docker Desktop is running. Open Terminal (or Windows Terminal) and navigate to the directory where your app files and the Dockerfile are located (if you have followed the tutorial, you should already be in the correct directory).

```bash
cd path/to/your/folder
```

Run the Docker command to build your image as shown below. Note that the dot at the end of the command is important. Please note that building the image may take a while.

```bash
docker build --platform linux/amd64 -t <some-name>:<some-tag> .
```
Replace `<some-name>:<some-tag>` with the name of the app and some tag to identify this particular version. For instance `my-gradio-app:v1.0`. 
Once the process is complete, run the following command in the Terminal. You should see your image in the list.

```bash
docker image ls
```

In order to test that the image you just built works you need to run a container from this image. To do that, run the following command in the Terminal.

```bash
docker run --rm -it -p 7860:7860 <some-name>:<some-tag>
```

If everything went well, you should now be able to navigate to `http://localhost:7860` in your browser and see and interact with your app.

### Publish your Docker image

You have now built and tested an image for your app on your computer. In order to be able to host this image on SciLifeLab Serve it needs to be published in a so-called image registry. Below, we show how to publish your image on [DockerHub](https://hub.docker.com) as an example but you can choose any public image registry (for example, on GitHub).

Register on [DockerHub](https://hub.docker.com/) (if you haven't done so already) and sign in with your account on Docker Desktop app.

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

This should publish your image on `https://hub.docker.com/r/<your-dockerhub-username>/<some-name>`. For example, our example app image for the flower image classification app is available on `ghcr.io/scilifelabdatacentre/gradio-flower-classification:20260206-185820`. Please note that your image should stay available even after your app is published on Serve because it will be fetched with regular intervals.

!!!warning "Note"

    Image push to the dockerhub repository might take quite a bit of time due to a multitude of factors. If this is the case for you you are welcome to move on to the next part and use the image ```ghcr.io/scilifelabdatacentre/gradio-flower-classification:20260206-185820``` to complete the next part of the tutorial.

## Hosting your application on SciLifeLab Serve

### Create a user account

If you do not already have a user account on SciLifeLab Serve, [create an account](https://serve.scilifelab.se/signup/).

### Create a project

Every app and model has to be located within a project. Projects that you have created/been granted access to can be found under **[My projects](https://serve.scilifelab.se/projects/)** page.

You need to be logged in to create a project. To create a project, click on the corresponding button on that page. Choose blank/default project if asked. The name and description of the project are visible only to you and those who you grant access to the project. Once the project is created, you will be taken to the project dashboard where you can create different types of apps.

### Create an app

In order to host an app that we just built click the Create button on the **Gradio App** card. Then enter the following information in the form:

* **Subdomain:** This is the subdomain that the deployed app will be available at (e.g., a subdomain of r46b61563 would mean that the app would be available at r46b61563.serve.scilifelab.se). If no subdomain name is entered, a random name will be generated by default. By clicking on New you can specify the custom subdomain name of your choice (provided that it is not already taken). This subdomain will then appear in the Subdomain options and the subdomain will appear in the format `name-you-chose.serve.scilifelab.se`.
* **Port:** The port that the your app runs on (in case of our template it will be `7860`).
* **Image:** Name of the image on DockerHub or full URL to the image on a different repository (this will be either `<your-dockerhub-username>/<some-name>:<some-tag>` if you are able to push the image or `ghcr.io/scilifelabdatacentre/gradio-flower-classification:20260206-185820` if you want to use an already built image).
* **Name:** Name of the app that will be displayed on the Public apps page.
* **Description:** Provide a brief description of the app, will also be displayed on the Public apps page.
* **Permissions:** The permissions for the app. There are four levels of permissions you can choose from:
  - **Private:** The app can only be accessed by the user that created the app (sign in required). Please note that we only allow the permissions to be set to Private temporarily, while you are developing the app. Eventually each app should be published publicly.
  - **Project:** All members of the project where the app is located will be able to access the app (sign in required). Please note that we only allow the permissions to be set to Project temporarily, while you are developing the app. Eventually each app should be published publicly.
  - **Link:** Anyone with the URL can access the app but this URL will not be publicly listed anywhere by us (this option is best in case you want to share the app with certain people but not with everyone yet).
  - **Public:** Anyone with the URL can access the app and the app will be displayed under Public apps page.
* **Source Code URL:** The link to source code for the application (you can put `https://github.com/ScilifelabDataCentre/gradio-flower-classification`)

You can leave the other fields as default.

## Congratulations!

Congratulations, you just built and started hosting your machine learning demo application!

Feel free to get in touch with the SciLifeLab Serve team with questions: serve@scilifelab.se.