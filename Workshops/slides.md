## Prerequisites

- Already work with ML/AI
- Python
- git
- text editor
- Docker Desktop 
- If you want to work on your own app: Python function that takes user input, does processing and inference using your model, and provides an output

## Part 1: building user interface for your app

### Preparation - spend 5 minutes on this

- Check that you have python 3.8 or higher $ python --version

```bash
python --version
git clone https://github.com/ScilifelabDataCentre/serve-tutorials
cd serve-tutorials/Workshops/Building-sharing-ML-demo-apps/
python -m venv .venv
source .venv/bin/activate
pip install gradio
```

Dedicate some time to people installing and setting up the environment. We will try to help you make it work but maybe it won't and then you'll just need to observe.

### Intro to Gradio

- Streamlit is an alternative

### Basic app

### Input and output types

### Multiple inputs and outputs

### Additional features

### Customization of the look of your app

### Performance

### Hands-on work

Dedicate some time to building a user interface. Two options:

Option 1. Use our prepared function (our image classification function) and build an app to meet our specifications. In your app, use custom theme, provide examples, enable progress bar, etc.... so that participants can make it more and more complex as they go.

Option 2. Try using gradio with your own function that you prepared.

## Part 2: Packaging your application as a Docker image

### Intro to Docker

- Docker Desktop
- Image repositories: DockerHub or GitHub

### What is needed - Dockerfile, requirements.txt, app app files

### Building Docker image

### Publishing Docker image

### Demo [? alternatively Hands-on work (two options - package our app or your own)]

- Show the files
- Build the image
- Publish the image

## Part 3: Hosting your application on SciLifeLab Serve

This is simply a demo. If someone wants to do it hands-on they can follow the steps written in the tutorial.