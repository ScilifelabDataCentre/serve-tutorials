## Welcome

While people are coming in: How are you doing?

<img data-src="assets/images/menti_qr.png" height="420" />


or go to [menti.com](https://menti.com/) and use code 5536 6348

---

## Building and sharing AI applications within ecology and biodiversity

---

## Who we are

- SciLifeLab -> SciLifeLab Data Centre -> SciLifeLab Serve team
- Today:
    - Hamza Imran Saeed
    - Jana Awada
- serve@scilifelab.se

---

<div style='position: relative; padding-bottom: 56.25%; padding-top: 35px; height: 0; overflow: hidden;'><iframe sandbox='allow-scripts allow-same-origin allow-presentation' allowfullscreen='true' allowtransparency='true' frameborder='0' height='315' src='https://www.mentimeter.com/app/presentation/aln14wtiajbx32kfwp6udrhqnnuot9bo/embed' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%;' width='420'></iframe></div>

---

### Making models available for inference

- Many models in biodiversity and ecology community.
- Some are useful for generating predictions on new input/new data.
- <b>Why make a model available for inference?</b>
  - Evaluation/verification of a model by the colleagues/community
  - Can be used as part of analysis workflows
  - Useful for general public or government agencies
  - Demo in an early commercialisation effort

---
<span style="color:red">How can one make a model available for inference?</span>

A trained ML model can be turned into a web application and made available on a URL.

---

## Today's plan

- Part 1. Building a user interface for an ML model
- Break 
- Part 2. Packaging and Hosting your application

---

## Part 1: Building a user interface for a model

---
<style>

code {
    color: #b93d59f2;
    font-weight: 580;
}
.code{
    color: #4e9098;
    font-weight: 580;
}
.container{
    display: flex;
}
.col{
    flex: 1;
    font-size: 30px;
}
.rounded {
    border-radius: 4px;
} 
</style>

### Web Frameworks for building user interfaces

  <table style="width:100%; border-collapse: separate; border-spacing: 24px;">
    <tr>
      <!-- Gradio -->
      <td style="vertical-align: top; border: 1px solid rgba(255,255,255,0.18); border-radius: 12px; padding: 16px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
          <img src="assets/images/gradio-logo.svg"
               alt="Gradio logo" style="height:40px;">
          <strong>Gradio</strong>
        </div>
        <p><strong>Best for:</strong> Quick ML demos</p>
        <p><strong>Pros:</strong> Very low code</p>
        <p><strong>Cons:</strong> Limited UI control</p>
      </td>
      <!-- Streamlit -->
      <td style="vertical-align: top; border: 1px solid rgba(255,255,255,0.18); border-radius: 12px; padding: 16px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
          <img src="assets/images/streamlit-logo.svg"
               alt="Streamlit logo" style="height:40px;">
          <strong>Streamlit</strong>
        </div>
        <p><strong>Best for:</strong> Data apps &amp; dashboards</p>
        <p><strong>Pros:</strong> Pythonic &amp; flexible</p>
        <p><strong>Cons:</strong> More code than Gradio</p>
      </td>
      <!-- Dash -->
      <td style="vertical-align: top; border: 1px solid rgba(255,255,255,0.18); border-radius: 12px; padding: 16px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
          <img src="assets/images/dashapp-logo.svg"
               alt="Plotly logo" style="height:40px;">
          <strong>Dash (Plotly)</strong>
        </div>
        <p><strong>Best for:</strong> Complex dashboards</p>
        <p><strong>Pros:</strong> Powerful &amp; scalable</p>
        <p><strong>Cons:</strong> Steeper learning curve</p>
      </td>
    </tr>
  </table>


---

### Gradio

- Open source framework
- Create web apps with Python code only
- Tailored to ML researchers
- Active community; tutorials online

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

```python [4-14]
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

### Gradio supports

<div class="container">
    <div class="col" style="font-size: 2.5rem!important;">
    <ul style="list-style-type: disc;">
      <li>Textbox</li>
      <li>Number</li>
      <li>Image</li>
      <li>Audio</li>
      <li>Video</li>
    </ul>
    </div>
    <div class="col" style="font-size: 2.5rem!important;">
    <ul style="list-style-type: disc;">
      <li>Slider</li>
      <li>Dropdown</li>
      <li>Files</li>
      <li>Dataframes</li>
      <li>…and more</li>
    </ul>
    </div>
</div>

---
### Multiple inputs and multiple outputs

```bash
python example_apps/multiple_inputs_app.py
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
python example_apps/examples_app.py
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

### Customization of the look of your app

Title, description, reference:

```bash
python example_apps/metadata_app.py
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

### Performance

Built-in queueing system:

- Max number of requests in queue
- Max number of threads
- Improved hardware

---

## Time for hands-on work

Tutorial: [https://sbdi-workshop.serve.scilifelab.se/](https://sbdi-workshop.serve.scilifelab.se/)

- **Option 1:** build a Gradio app for our model
    - The example app is in the `hands_on_app` folder
    - Install the packages from `hands_on_app/requirements.txt`
    - Download and copy the data to `hands_on_app/data/flower_model_vgg19.pth`
    - Add a Gradio app to `hands_on_app/main.py`
    - Make your app fancy!
- **Option 2:** build a Gradio app for your own model/function


---

## Part 2: Packaging your application and hosting it on Scilifelab Serve

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

---

### Structure

You can continue working in `hands-on-app` directory.


The directory has the following structure as you have seen in the hands-on session:

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
---

### Docker basic commands

- **`docker images`** : Lists all Docker images on the local machine
- **`docker pull {name}:{tag}`**: Pull image from a registry
- **`docker run {name}:{tag}`**: Download image from a registry and run container
- **`docker build -t {name}:{tag} .`**: Builds a Docker image from a Dockerfile in the current directory


---

### SciLifeLab Serve

- https://serve.scilifelab.se/;
- Platform for hosting applications and machine learning models;
- Free to use for life science researchers affiliated with a Swedish research institution and their international collaborators;
- Each app receives 2 vCPU, 4GB RAM by default; more can be requested with demonstrated need.

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