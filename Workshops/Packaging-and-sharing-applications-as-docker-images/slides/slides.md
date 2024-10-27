## Welcome

While people are coming in: How are you doing?

<img data-src="menti_qr.png" height="420" />

<!-- TODO: Update link -->

or go to [menti.com](https://menti.com/) and use code XXXX XXXX

---

## Packaging and sharing data science applications as Docker container images

---

## Who we are

- SciLifeLab -> SciLifeLab Data Centre -> SciLifeLab Serve team
- Today:
    - Johan Alfredéen
    - Hamza Imran Saeed
- serve@scilifelab.se

---

## Who you are

<img data-src="menti_qr.png" height="420" />

<!-- TODO: Update link -->

or go to menti.com and use code XXXX XXXX

---

<!-- TODO: Update link -->

<section data-background-iframe="https://www.mentimeter.com/app/presentation/alhxr8rtvrksuu9ni6egtmkde8zzx7iu/embed" data-background-interactive>
</section>


---

Find the written tutorial for today here:

<img data-src="tutorial_qr.png" height="420" />

[bit.ly/47vwato](http://bit.ly/47vwato)

---
## Today's plan

<!-- TODO: This slide could be made less intimidating -->

- Part 1. Introduction to Docker Containers
    - Basics and example apps (35 minutes)
    - Hands-on part (20 minutes)
- Break (10 minutes)
- Part 2. Packaging your application as a Docker image (demo, 15 minutes)
- Part 3. Hosting your application on SciLifeLab Serve (demo, 15 minutes)
- More hands-on + Q&A, wrap-up (remaining time)

---

## Part 1: Introdcution to Docker Containers

---

### What is a Docker?

- Open-source tool
- OS-level virtualization to deliver software in packages called containers
- Simplifies development and deployment processes
- Ensures reproducibility and scalability
- Facilitates collaboration by sharing environments

---

#### Containers: packages of your application code together with dependencies

---
### Containers in software development

- Portability:
  - Consistent behavior across different environments
  - Eliminates “it works on my machine” issues
- Efficiency:
  - Uses fewer resources than traditional VMs
  - Faster startup times and better resource utilization
- Isolation:
  - Independent running environments
  - Prevents conflicts between applications and dependencies
- CI/CD Simplification:
  - Consistent environment for testing and deployment
  - Accelerates development cycles and improves software quality
- Extensive Ecosystem:
  - Access to a vast repository of pre-built images on Docker Hub
  - Quick deployment of a wide range of applications and services

---

### Without Containers
- Clone GitHub repository or get code from an external source;
- Setup Environment and Install, uninstall packages and dependencies;
- Download data;

---

### With Containers
- Standardized, self contained packaged software;
- Platform-agnostic (Linux, Mac, Windows);
- Many different container engines are available. Docker is the most popular and widely used;
- Other engines: Podman, Apptainer, Enroot, many more...   

---

### Container repositories

- What are Container Repositories?
    - Storage locations for Docker images.
    - Enable sharing and distribution of images.
- Types of Repositories:
    - Public Repositories: Accessible by anyone.
    - Private Repositories: Restricted access for specific users or teams.
- Benefits:
    - Centralized storage for images.
    - Facilitates collaboration and sharing.
    - Simplifies deployment processes.

---

### DockerHub

- The largest public repository for Docker images
- Hosted by Docker Inc.
    - Enable sharing and distribution of images.
- Public and Private Repositories: Store images with varying access levels
- Automated Builds: Automatically build images from GitHub or Bitbucket repositories
- Official Images: Curated and maintained, ensuring high quality and security


---
### Writing a Dockerfile

To build a Docker image, you need to create a Dockerfile. It is a plain text file with instructions and arguments. Here is the description of the instructions we're going to use in our next example:

- FROM -- set base image
- RUN -- execute command in container
- ENV -- set environment variable
- WORKDIR -- set working directory
- COPY -- copy files into the container
- ENTRYPOINT -- specifies the command that will always be executed when a container starts


---

### Dockerfile Example

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
WORKDIR $HOME

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common

# Copy code and start script (this will place the files in home/username/)
COPY requirements.txt $HOME/requirements.txt
COPY main.py $HOME/main.py
# copy any other files that are needed for your app with the directory structure as your files expect
COPY start-script.sh $HOME/start-script.sh
COPY data/ $HOME/app/data

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x start-script.sh \
    && chown -R $USER:$USER $HOME \
    && rm -rf /var/lib/apt/lists/*

USER $USER
EXPOSE 7860

ENTRYPOINT ["./start-script.sh"]

```

---

### Customization of the look of your app

Title, description, reference:

```bash
gradio example_apps/hello4_app.py
```

```python [17-20]
import gradio as gr

def greet(name):
   return "Hello " + name + "!"

title = "Demo app"
description = (
  "<center>"
  "Text, images, etc. can be added here with HTML or markdown formatting."
  "</center>"
)
ref = "This app is related to the following article: [Article title](#). The code can be found here: [GitHub](#)"

demo = gr.Interface(fn=greet, 
                    inputs="text", 
                    outputs="text", 
                    title=title, 
                    description=description, 
                    article=ref)

demo.launch(server_name="0.0.0.0", server_port=7860)
```

---

Themes: pre-built or make your own

```python
demo = gr.Interface(fn=greet, inputs="text", outputs="text", theme=gr.themes.Soft())
```

https://www.gradio.app/guides/theming-guide

----

Gradio Blocks: https://www.gradio.app/docs/blocks

---

### Performance

Built-in queueing system:

```python
demo.queue().launch(server_name="0.0.0.0", server_port=7860)
```

- Max number of requests in queue
- Max number of threads
- Improved hardware

---

## Time for hands-on work

- **Option 1:** build a Gradio app for our model/function
    - The example app/model is in the `hands_on_app/folder`
    - Install the packages from `hands_on_app/requirements.txt`
    - Download and copy the data to `data/flower_model_vgg19.pth`
    - Add a Gradio app to `hands_on_app/main.py`
    - Make your app fancy!
- **Option 2:** build a Gradio app for your own model/function

---

## Part 2: Packaging your application as a Docker Container Image

---

#### Containers: packages of your application code together with dependencies

---

### Without Containers
- Clone GitHub repository or get code from an external source;
- Setup Environment and Install, uninstall packages and dependencies;
- Download data;

---

### With Containers
- Standardized, self contained packaged software;
- Platform-agnostic (Linux, Mac, Windows);
- Many different container engines are available. Docker is the most popular and widely used;
- Other engines: Podman, Apptainer, Enroot, many more...   

---

### Pre requisites for deployment

- To host your app on SciLifeLab Serve, you first need to package it as a Docker image.
- If you don't have docker, you can install it from [docs.docker.com/get-docker](https://docs.docker.com/get-docker/).

---
### Image classification example app
- The model we will use in this example is a [Flowers Classification Model PyToch model](https://github.com/ScilifelabDataCentre/serve-tutorials/tree/main/Webinars/2023-Using-containers-on-Berzelius/flowers-classification) based on the [102 Category Flower Dataset](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/);
- You can follow the instructions mentioned in the [README](https://github.com/ScilifelabDataCentre/serve-tutorials/tree/main/Workshops/Building-sharing-ML-demo-apps) file in the GitHub repository to train the model your self but keep in mind it takes quite a while (~ 4 hours) with limited CPUs. 

<!-- TODO: Link can add qr code to menti for the link to GitHub. -->

---

### Structure
The code for the app and the Dockerfile used to build the app is available in the `image_classification_app/` folder inside the [serve-tutorials](https://github.com/ScilifelabDataCentre/serve-tutorials/tree/building-sharing-ML-demo-apps/Workshops/Building-sharing-ML-demo-apps) repository.


The directory has the following structure:

```bash
..
├── requirements.txt
├── main.py
├── data   
    └── ... (model and any other static files required)
├── ... (any other files your app requires)
├── start-script.sh
└── Dockerfile
```

---

### Dockerfile

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
WORKDIR $HOME

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common

# Copy code and start script (this will place the files in home/username/)
COPY requirements.txt $HOME/requirements.txt
COPY main.py $HOME/main.py
# copy any other files that are needed for your app with the directory structure as your files expect
COPY start-script.sh $HOME/start-script.sh
COPY data/ $HOME/app/data

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x start-script.sh \
    && chown -R $USER:$USER $HOME \
    && rm -rf /var/lib/apt/lists/*

USER $USER
EXPOSE 7860

ENTRYPOINT ["./start-script.sh"]

```
---

### Main.py

The main file for the Gradio app

```python
import gradio as gr
import torch
from PIL import Image
from torchvision import transforms
import torchvision.models as models

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

interface = gr.Interface(fn=predict,
             inputs=gr.Image(type="pil"),
             outputs=gr.Label(num_top_classes=3))

interface.launch(server_name="0.0.0.0", server_port=7860)
```

---

### Start script

Deployment on Serve requires a script that will be launching your application. Create a file *start-script.sh* and put it in the same directory as your app.

```bash
#!/bin/bash

python main.py
```

---

Demo

---

## Part 3: Publishing your app on SciLifeLab Serve

---

### SciLifeLab Serve

- https://serve.scilifelab.se/;
- Platform for hosting applications and machine learning models;
- Free to use for life science researchers affiliated with a Swedish research institution and their international collaborators;
- Each app receives 2 vCPU, 4GB RAM by default; more can be requested with demonstrated need.

---

Demo

---

## Time for hands-on work

We are happy to help and answer questions. 

Options:
- Continue working on your app
- Try packaging your app as a Docker image
- Try publishing an app on SciLifeLab Serve

---

## That's it from us. Thank you!

Please fill out the evaluation form you will receive by email.

---

## Syntax highlighting

```python
def hello_world():
    print("Hello world!")
```

Press down

----

## Highlight lines

```python [1|3-6]
n = 0
while n < 10:
  if n % 2 == 0:
    print(f"{n} is even")
  else:
    print(f"{n} is odd")
  n += 1
```

---

# Slide with two columns

<div class="container">
    <div class="col">
        <p>Column 1</p>
    </div>
    <div class="col">
        <p>Column 2</p>
    </div>
</div>

---
# How to make stuff appear on by one

Use "fragmet" class

```html
<p class="fragment">This will appear first</p>
<p class="fragment">This will appear second</p>
```

<p class="fragment">This will appear first</p>
<p class="fragment">This will appear second</p>

---

# Using pyscript

<button id="my_button">Click me!</button>
<div id="output-py"></div>
<py-script>
from pyscript import when, display
@when("click", "#my_button")
def click_handler(event):
    display("I've been clicked!", target="output-py")
</py-script>

----

## Adding a hover button that would show code snippet
<py-script>
from pyscript import when, display
@when("click", "#my_button-1")
def click_handler_1(event):
    display("I've been clicked!", target="output-py-1")
</py-script>
<div>
    <button id="my_button-1">Click me!</button>
    <div class="info-icon">
        <!-- if you have fontawesome installed -->
        <!-- <i class="fa-solid fa-code fa-lg"></i> -->
        Hover over me
        <div style="width: 600px" class="tooltip">
            <div class="code-snippet">
                <pre style="all: initial; font-size: 20px">
                <code>
<py-script>
from pyscript import when, display
@when("click", "#my_button-1")
def click_handler_1(event):
    display("I've been clicked!", target="output-py-1")
</py-script>
                </code>
            </div>
        </div>
    </div>
</div>
<div id="output-py-1"></div>


