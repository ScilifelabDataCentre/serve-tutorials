# Building and sharing machine learning demo applications in life sciences: a practical tutorial

---

## Welcome

---

## Who we are

- Who we are

---

## Target audience of this workshop

- Target audience of this workshop

---

## Today's plan

- Part 1. Building a user interface for your model
    - Basics and example apps (35 minutes)
    - Hands-on part (20 minutes)
- Break (10 minutes)
- Part 2. Packaging your application as a Docker image (demo, 15 minutes)
- Part 3. Hosting your application on SciLifeLab Serve (demo, 15 minutes)
- More hands-on + Q&A, wrap-up (remaining time)

---

## Part 1: Using Gradio to build a user interface

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
gradio example_apps/hello_app.py
```

Navigate to http://0.0.0.0:8080

App code:

```python [1|3-4|6|8]
import gradio as gr

def greet(name):
   return "Hello " + name + "!"

interface = gr.Interface(fn=greet, inputs="text", outputs="text")

interface.launch(server_name="0.0.0.0", server_port=8080)
```

---

### Input and output types

Image input and output:

```bash
gradio example_apps/sepia.py
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

interface = gr.Interface(fn=sepia, inputs=gr.Image(), outputs="image")

interface.launch(server_name="0.0.0.0", server_port=8080)
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
- radio buttons
- files
- dataframes
- etc.

---
### Multiple inputs and multiple outputs

```bash
gradio example_apps/hello2_app.py
```

```python [11-12]
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
)

demo.launch(server_name="0.0.0.0", server_port=8080)
```

---

### Additional features

Providing examples

```bash
gradio example_apps/hello3_app.py
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

demo.launch(server_name="0.0.0.0", server_port=8080)
```

----

Progress bar

```bash
gradio example_apps/progress_app.py
```

```python [4-9]
import gradio as gr
import time

def my_function(x, progress=gr.Progress()):
    progress(0, desc="Starting...")
    time.sleep(1)
    for i in progress.tqdm(range(100)):
        time.sleep(0.1)
    return x

demo = gr.Interface(fn=my_function, inputs=gr.Textbox(), outputs=gr.Textbox())

demo.queue().launch(server_name="0.0.0.0", server_port=8080)
```
----

Access through API

- Custom Python and JavaScript clients for Gradio
- REST API endpoint `/predict/api`
- Can be disabled:

```python
demo.launch(server_name="0.0.0.0", server_port=8080, show_api=False)
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
gradio example_apps/hello4_app.py
```

```python [18-20]
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

demo.launch(server_name="0.0.0.0", server_port=8080)
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

```python
demo.queue().launch(server_name="0.0.0.0", server_port=8080)
```

- Max number of requests in queue
- Max number of threads
- Improved hardware

---

## Time for hands-on work

Option 1: build a Gradio app for our model/function

Option 2: build a Gradio app for your own model/function

---

## Part 2: Packaging your application as a Docker image

---

### Image classification example app

---

## Part 3: Publishing your app on SciLifeLab Serve

---

### SciLifeLab Serve

- https://serve.scilifelab.se/
- Platform for hosting applications and machine learning models
- Free to use for life science researchers affiliated with a Swedish research institution and their international collaborators
- Each app receives 2 vCPU, 4 RAM by default; more can be requested with demonstrated need

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


