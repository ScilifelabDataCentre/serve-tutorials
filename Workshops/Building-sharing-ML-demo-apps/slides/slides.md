## Welcome

While people are coming in: How are you doing?

<img data-src="menti_qr.png" height="420" />

<!-- TODO: Update link -->

or go to [menti.com](https://menti.com/) and use code 1967 8095

---

## Building and sharing machine learning demo applications: a practical tutorial

---

## Who we are

- Today's event is co-organised with KTH Library 🎉
- SciLifeLab -> SciLifeLab Data Centre -> SciLifeLab Serve team
- Today:
    - Arnold Kochari
    - Johan Alfredéen
    - Mahbub Ul Alam
- serve@scilifelab.se

---

## Who you are

<img data-src="menti_qr.png" height="420" />

<!-- TODO: Update link -->

or go to menti.com and use code 1967 8095

---

<!-- TODO: Update link -->

<section data-background-iframe="https://www.mentimeter.com/app/presentation/alpptrbomxo6upjcheatsf14qtn913ni/embed" data-background-interactive>
</section>

---
## Today's plan

- Intro
- Part 1. Creating a web application from an ML model 
- Break 
- Part 2. Packaging your application as a Docker image
- Part 3. Hosting your application on SciLifeLab Serve

---

## Intro

---

## Part 1: Using Gradio to build a web application

---

### Gradio

- Open source framework
- Create web apps with Python code only
- Tailored to ML researchers
- Active community; tutorials online
- Alternatives: Streamlit, Dash, FastAPI, Flask, etc.

---

Find the written tutorial for today here:

[bit.ly/ml-apps-tutorial](http://bit.ly/ml-apps-tutorial)

---


### Preparation

```bash
python --version
git clone https://github.com/ScilifelabDataCentre/serve-tutorials
cd serve-tutorials/Workshops/Building-sharing-ML-demo-apps/
python -m venv .venv
source .venv/bin/activate
pip install gradio
```

---

### Simplest application with Gradio

To run this app:

```bash
python example_apps/hello_app.py
```

Navigate to http://0.0.0.0:7860

App code:

```python [1|3-4|6|8]
import gradio as gr

def greet(name):
   return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch(server_name="0.0.0.0", server_port=7860)
```

---

### Input and output types

Image input and output:

```bash
python example_apps/sepia_app.py
```

```python [14]
import numpy as np
import gradio as gr

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

demo = gr.Interface(fn=sepia, inputs=gr.Image(), outputs=gr.Image())

demo.launch(server_name="0.0.0.0", server_port=7860)
```

----

Specifying labels for input and output

```python
demo = gr.Interface(fn=sepia, 
                    inputs=gr.Image(label="Your image"), 
                    outputs=gr.Image(label="Sepia filtered image")
                    )
```

----

Gradio supports:
- textbox
- number
- image
- audio
- video 
- slider
- dropdown 
- files
- dataframes
- etc.

---
### Multiple inputs and multiple outputs

```bash
python example_apps/hello2_app.py
```

```python [3,7,11-12]
import gradio as gr

def greet(name, is_morning, temperature_F):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature_F} degrees today"
    celsius = (temperature_F - 32) * 5 / 9
    return greeting, round(celsius, 2)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "number"]
)

demo.launch(server_name="0.0.0.0", server_port=7860)
```

---

### Additional features

Providing examples

```bash
python example_apps/hello3_app.py
```

```python [11,13]
import gradio as gr

def greet(name, is_morning, temperature_F):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature_F} degrees today"
    celsius = (temperature_F - 32) * 5 / 9
    return greeting, round(celsius, 2)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "number"],
    examples=[["David", True, 55], ["Ash", False, 70]]
)

demo.launch(server_name="0.0.0.0", server_port=7860)
```

----

Custom input and output components

https://www.gradio.app/custom-components/gallery

----

Access through API

- REST API endpoint
- Custom Python and JavaScript clients for Gradio
- Can be disabled:

```python
demo.launch(server_name="0.0.0.0", server_port=7860, show_api=False)
```

----

Inference without clicking the 'submit' button

```python
demo = gr.Interface(fn=greet, inputs="text", outputs="text", live=True)
```

---

### Customization of the look of your app

Title, description, reference:

```bash
python example_apps/hello4_app.py
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

----

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

- Max number of requests in queue
- Max number of threads
- Improved hardware

---

## Time for hands-on work

- **Option 1:** build a Gradio app for our model
    - The example app is in the `hands_on_app` folder
    - Install the packages from `hands_on_app/requirements.txt`
    - Download and copy the data to `hands_on_app/data/flower_model_vgg19.pth`
    - Add a Gradio app to `hands_on_app/main.py`
    - Make your app fancy!
- **Option 2:** build a Gradio app for your own model/function

---

## Part 2: Packaging your application as a Docker Container Image

---

### Prerequisites for sharing your app

- To send your application or to make it available online you first need to package it 
- Docker is a powerful and popular way to do it
- If you don't have docker, you can install it from [docs.docker.com/get-docker](https://docs.docker.com/get-docker/).

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

### Image classification example app
- The model we will use in this example is a [Flowers Classification Model PyToch model](https://github.com/ScilifelabDataCentre/serve-tutorials/tree/main/Webinars/2023-Using-containers-on-Berzelius/flowers-classification) based on the [102 Category Flower Dataset](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/);
- You can follow the instructions mentioned in the [README](https://github.com/ScilifelabDataCentre/serve-tutorials/tree/main/Workshops/Building-sharing-ML-demo-apps) file in the GitHub repository to train the model yourself but keep in mind it takes quite a while (~ 4 hours) with limited CPUs. 

<!-- TODO: Link can add qr code to menti for the link to GitHub. -->

---

### Structure

All files required for our app are available in the folder `image_classification_app/flower_classification`


The directory has the following structure:

```bash
..
├── requirements.txt
├── main.py
├── data   
    └── ... (model and any other static files required)
├── ... (any other files your app requires)
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

# Copy all files that are needed for your app with the directory structure that your app expects
COPY requirements.txt $HOME/requirements.txt
COPY main.py $HOME/main.py
COPY data/ $HOME/app/data

RUN pip install --no-cache-dir -r requirements.txt \
    && chown -R $USER:$USER $HOME \
    && rm -rf /var/lib/apt/lists/*

USER $USER

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "main.py"]
```
---

### main.py

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


