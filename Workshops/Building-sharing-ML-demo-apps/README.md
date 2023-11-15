# Building and sharing machine learning demo applications within life sciences: a practical tutorial

During the tutorial we will start from a trained model and demonstrate step by step how you can create a graphical user interface for your application, prepare it for deployment, and make it available on the web with a URL. The target audience of this tutorial are researchers working with machine learning models that do not have web development background but still want to share demos of their models as web applications. We will demonstrate the use of specific tools which make this process easy.

Note that the setup described here will cover the needs of a large majority of researchers when they want to share their ML model, allowing to give the app users instant predictions and good performance overall. In the minority of cases performance might be an issue when using this approach - perhaps your model is really large and needs a lot of time or resources to make predictions or you care about fast inference down to milliseconds. In these latter cases there are more specialized ways to build or serve applications, those cases are not covered here.

## Step 0. Creating a prediction function with your model

Before you can start building a user interface for your app, you need to have a function that takes input, uses your trained model to make a prediction, and gives output. Exactly what kind of processing happens inside that function does not matter for the user interface that we will be building, it will only care about the input(s) and output(s). We do not cover this part in the tutorial since it will be different for different ML frameworks.

## Step 1. Building a user interface

There are multiple frameworks that simplify the process of building apps with graphical user interfaces for machine learning model. For example, [Gradio](https://github.com/gradio-app/gradio) and [Streamlit](https://github.com/streamlit/streamlit) are such open source frameworks with a good community around them. In this tutorial we make use of Gradio. Here we will only cover basic functionality of Gradio which should suffice for most of the needs of researchers in life sciences. We want to note that Gradio (as well as Streamlit) offers niche functionality and flexibility for specific use cases so be sure to check [the official documentation](https://www.gradio.app/docs/) once you learn the basics here.

In this tutorial we use examples from the official [Gradio documentation](https://www.gradio.app/guides/quickstart) as well as custom examples that we created ourselves.

### Preparation

In order to follow this tutorial, make sure that you are running Python 3.8 or later. Clone the repository that we prepared, create a virual environment, and install the [gradio](https://pypi.org/project/gradio/) package.

```bash
python --version
git clone https://github.com/ScilifelabDataCentre/serve-tutorials
cd serve-tutorials/Workshops/Building-sharing-ML-demo-apps/
python -m venv .venv
source .venv/bin/activate
pip install gradio
```

If all is successful, you are now ready to start looking at the examples the `example_apps/` folder and trying out different things in the templates that we prepared.

### Simplest application with Gradio

We start with the basic case where the user provides custom input in a text field and receive output in text format. This example is in the `example_apps/hello_app.py` file. Let's first run it and see what it gives us. To run this and all the subsequent apps in this tutorial you can enter the following in the terminal:

```bash
gradio example_apps/hello_app.py
```

Once it is running you should see that it is available under http://0.0.0.0:8080. Navigate to this link in your browser and try out the app.

Let's take a closer look at what the code in this file does.

```python
import gradio as gr

def greet(name):
   return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch(server_name="0.0.0.0", server_port=8080)
```

We start by importing the *gradio* package. We define the function that Gradio will use. This simple function takes one input and returns one output.

Using the *Interface* class we define what the app should look like. We pass the following parameters: *fn* specifies the function that the app should be running, *inputs* specifies what fields the user should be allowed to give as input, *output* specifies what kind of output the function will be showing the user.

Finally, the launch method instructs to launch the defined app and we specify that we want it to run on port 8080.

This example demonstrates the three basic components that your app will need - the function that the app will be based on, the interface definition, and the launch command. We will now build on this simplest case to add more complex scenarios and customize the app.

### Input and output types

We saw how Gradio can work with text input and output. In the example `example_apps/sepia_app.py` we can see how it can take an image input and provide an image output. We do this by changing the *inputs* and *outputs* parameters in the interface definition.

```python
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

demo = gr.Interface(fn=sepia, inputs=gr.Image(), outputs="image")

demo.launch(server_name="0.0.0.0", server_port=8080)
```

Gradio supports [a large number of other input and output types](https://www.gradio.app/docs/components), called *components*. For example, text, textbox, number, image, audio, video, slider, dropdown, radio buttons, files, dataframes, and so on. Different types of inputs and outputs can of course be combined - for example, a user can upload an image and receive a classification score as an output, we give an example of this below.

In order to change the label displayed to the user in the input or output fields, you can simply add a *label* argument to the inputs and outpus, as shown below.

```python
interface = gr.Interface(fn=sepia, inputs=gr.Image(lable="Your image"), outputs=gr.Image("Sepia filtered image"))
```

### Multiple inputs and multiple outputs

It is also possible to allow users to provide multiple inputs and receive multiple outputs. In the example `example_apps/hello2_app.py` the user provides a text input, a checkbox input, as well as a number input and receives text and number output.

```python
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

Note that the number and the order of input and output parameters in the function *greet* and in the Gradio interface definition match.

### Additional features

Now that we looked at the basics let's take a look at some of the ways in which you can make your app more user-friendly. Gradio comes with many features, we will only highlight a few.

#### Providing examples

You might want to provide example inputs for your app so that the users can try it out quickly or know how to prepare their input. This can be done by simply adding an *[examples](https://www.gradio.app/docs/examples)* argument to your interface definition. You can see an example of this in `example_apps/hello3_app.py`.

#### Progress bar

Gradio provides a [custom progress tracker](https://www.gradio.app/docs/progress) that can be added to your function to show how far the processing has gone. This is demonstrated in the example `example_apps/progress_app.py`.

#### Access through API

By default the apps created and published with Gradio also provide information on how it can be accessed using an API through custom Python and JavaScript clients. At the bottom of the app there is a link "Use via API" which gives instructions how the app can be accessed using these clients. This can be disabled by setting *show_api* to *False* in the app launch command, as shown below.

```python
demo.launch(server_name="0.0.0.0", server_port=8080, show_api=False)
```

A REST API endpoint is also created automatically though it is not described in the user interface in the latest version of Gradio; the REST API endpoint is `/predict/api`.

#### Inference without clicking the 'submit' button

If you don't want your users to have to click on "Submit" to get a prediction result, you can simply pass variable *live=True* in your interface defition, as shown below. We don't recommend doing this for all apps, however, because for example if your users are typing text you will be unnessarily loading the servers while the text is being typed (since your function execution will be triggered with every typed letter) rather than running an inference once at the end. Performance of your server might become an issue if your app becomes popular so you should keep that in consideration (see more info also below).

```python
demo = gr.Interface(fn=greet, inputs="text", outputs="text", live=True)
```

### Customization of the look of your app

You might want to add a title, description, etc. for your app that should be displayed alongside the input and output. These can be specified as parameters of the interface. Some of the options are: title, description, article, thumbnail, CSS (see [the Interface documentation](https://www.gradio.app/docs/interface) for all parameters). In the example `example_apps/hello4_app.py` we added some of these parameters.

There are multiple ways to change the visuals of a Gradio app.  One way to customize the look is to use [Gradio themes](https://www.gradio.app/guides/theming-guide). You can use one of the prebuilt themes (e.g. Glass, Monochrome, Soft) with your app or [create your own theme](https://www.gradio.app/guides/theming-guide). The theme can be set by simply specifying the *theme* variable in the interface defition as shown below.

```python
demo = gr.Interface(fn=greet, inputs="text", outputs="text", theme=gr.themes.Soft())
```

If you want to be even more flexible, Gradio offers [Blocks](https://www.gradio.app/docs/blocks). With blocks you can change the layout of the different components of your app, when the function is triggered, group multiple demos into tabs, etc.

We do not cover customization of your app further here because there are many possibilities. Please refer to the official documentation of Gradio for more info.

### Performance

In case your app becomes popular and you have many users coming to make predictions at the same time we want to make sure we can handle the load. One of the most useful aspects of using Gradio is provides some tools to help with performance out of the box. Specifically, it provides [a queueing system](https://www.gradio.app/guides/setting-up-a-demo-for-maximum-performance) that you can easily set up by adding the *.queue* method before you launch your app.

```python
demo.queue().launch(server_name="0.0.0.0", server_port=8080)
```

With queueing enabled each prediction request from the users will be put in a queue. When a worker becomes free, the first available request is passed into the worker for inference. When the inference is complete, the queue sends the prediction back to the particular Gradio user who called that prediction. It is also possible to set the maximum number of requests that are allowed to join the queue.

Another parameter that can be used to improve performance is the maximum number of worker threads in the Gradio server that can be processing requests at once.

Finally, performance will also depend on the hardware on which your app is running.

This is an advanced topic so we refer to [Gradio documentation for more information](https://www.gradio.app/guides/setting-up-a-demo-for-maximum-performance). If you are hosting your Gradio application on SciLifeLab Serve, get in touch with us and we can help you find the best Gradio parameters and hardware to improve performance.

### Image classification example app

Putting together some of the Gradio functionality described above we prepared an example image classification app to demonstrate how you can build apps with complex machine learning models behind. This example is `image_classificastion_app/main.py`. Here, we used.... TO BE WRITTEN TO BE WRITTEN TO BE WRITTEN TO BE WRITTEN. 

You can find other examples of image classification apps in the official Gradio documentation: [example with PyTorch](https://www.gradio.app/guides/image-classification-in-pytorch), [example with TensforFlow](https://www.gradio.app/guides/image-classification-in-tensorflow).

## Step 2. Packaging your application as a Docker image

There are multiple ways to host your application on a web server. Below, we demonstrate how to host on SciLifeLab Serve, a dedicated machine learning model and app hosting platform for life science researchers in Sweden that is free. To host your app on SciLifeLab Serve, you first need to package it as a Docker image. This is a simple process even if you have not done this before so do not worry. You can simply start with the template we provide, all necessary files are in the folder `image_classification_app/`.

You will need to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your computer to be able to build an image.

### Create start script

One additional component you need is a script that will be launching your application. In our example, the start script is simple. Create a file *start-script.sh* and put it in the same directory as your app.

```bash
#!/bin/bash

python main.py
```

### Create a Dockerfile

The other component you need is a Dockerfile. Dockerfile if a file containing instructions for how your Docker image should be built. See [the official documentation]((https://docs.docker.com/engine/reference/builder/)) if you are curious to learn more but for the purpose of hosting your app it is sufficient to simply copy and if needed adjust the template below. Note that this file should be called simply `Dockerfile`, without any file extension.

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
EXPOSE 8080

ENTRYPOINT ["./start-script.sh"]

```

This Dockerfile instructs to start with a base image containing Python version 3.11 (it is going to contain Ubuntu as operating system and components required to run Python), install the required packages listed in *requirements.txt*, copy all the scripts and other necessary files for the app into the image (copy your own files here as well), and, finally, points to the script to start the app. The Dockerfile also contains information about which user should be running the app and which port it should expose.

At this point, you should have the following file structure in your app directory:

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
### Adding models to the data folder

The models being used in these examples are publicly available and are listed below. You can chose which model you want to test and run follow the instructions to to download it.

#### Flowers Classification Model

This model has been trained on Scilifelab Serve and instructions on how to do that can be found [here](https://github.com/ScilifelabDataCentre/serve-tutorials/tree/main/Webinars/2023-Using-containers-on-Berzelius/flowers-classification). You can follow the instructions to train the model your self but keep in mind it takes quite a while (~ 4 hours) with limited CPUs. For information about the dataset used, [see](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/).

The app is configured to use the model from the data folder. To download the model to the data folder go into the directory

```bash
cd flower_classification/data/
```
then run the following command to download the model
```bash
curl -O -J https://nextcloud.dc.scilifelab.se/s/GSf2g5CAFxBPtMN/download
```

#### Resnet 18 Image Classification Model

This model has been obtained from the official [Pytorch Model Zoo](https://pytorch.org/serve/model_zoo.html). The models here are packaged as .mar archives to work conveniently with [TorchServe](https://pytorch.org/serve/). We have unpacked the archives and added the .pth files (which can be used to load the model) to nextcloud and can be downloaded as follows.

To download the model to the data folder go into the data directory
```bash
cd resnet_image_classification/data/
```
then run the following command to download the model
```bash
curl -O -J https://nextcloud.dc.scilifelab.se/s/6znJ2FPZPyLKaGa/download
```

#### VGG 11 Image Classification Model

This model has been obtained from and older verions of the [Pytorch Model Zoo](https://jlin27.github.io/serve-1/model_zoo.html). The models here are packaged as .mar archives to work conveniently with [TorchServe](https://pytorch.org/serve/). We have unpacked the archives and added the .pth files (which can be used to load the model) to nextcloud and can be downloaded as follows.

To download the model to the data folder go into the data directory
```bash
cd vgg11_image_classification/data/
```
then run the following command to download the model
```bash
curl -O -J https://nextcloud.dc.scilifelab.se/s/8FLB6JqJsPBDcWw/download
```

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
docker run --rm -it -p 8080:8080 <some-name>:<some-tag>
```

If everything went well, you should now be able to navigate to `http://localhost:8080` in your browser and see and interact with your app.

### Publish your Docker image

You have now built and tested an image for your app on your computer. In order to be able to host this image on SciLifeLab Serve it needs to be published in a so-called image registry. Below, we show how to publish your image on [DockerHub](https://hub.docker.com) as an example but you can choose any public image registry (for example, on GitHub).

Register on [DockerHub](https://hub.docker.com/) and sign in with your account on Docker Desktop app.

Next, re-build your image as described above, this time including your DockerHub username in the image name, as shown below. 

```bash
docker build -t <your-dockerhub-username>/<some-name>:<some-tag> .
```

Once the image is built and visible on Docker Desktop, pick *"Push to Hub"* among the options for your app image. Alternateively, you can also use the following command from the terminal instead

```bash
docker push <your-dockerhub-username>/<some-name>:<some-tag>
```
keep in mind the you might need to login to you dockerhub user incase you haven't done so already. This can be done as follows
```bash
docker login --username=<your-dockerhub-username>
```
This should publish your image on *https://hub.docker.com/r/&lt;your-dockerhub-username&gt;/&lt;some-name&gt;:&lt;some-tag&gt;*. For example, our example app image for the flower image classification app is available on `hamzaisaeed/gradio-workshop:flower_classification`. Please note that your image should stay available even after your app is published on Serve because it will be fetched with regular intervals.

## Step 3. Hosting your application on SciLifeLab Serve

### Create a user account on SciLifeLab Serve

If you do not already have a user account on SciLifeLab Serve, [create an account](https://serve.scilifelab.se/signup/).

### Create a project

Every app and model has to be located within a project. Projects that you have created/been granted access to can be found under **[My projects](/projects/)** page.

You need to be logged in to create a project. To create a project, click on the corresponding button on that page. Choose blank/default project if asked. The name and description of the project are visible only to you and those who you grant access to the project. Once the project is created, you will be taken to the project dashboard where you can create different types of apps.

### Create an app

In order to host an app that we just built click the Create button on the Custom app card. Then enter the following information in the form:

* **Name:** Name of the app that will be displayed on the Public apps page.
* **Description:** Provide a brief description of the app, will also be displayed on the Public apps page.
* **Subdomain:** This is the subdomain that the deployed app will be available at (e.g., a subdomain of r46b61563 would mean that the app would be available at r46b61563.serve.scilifelab.se). If no subdomain name is entered, a random name will be genrated by default. By clicking on New you can specify the custom subdomain name of your choice (provided that it is not already taken). This subdomain will then appear in the Subdomain options and the subdomain will appear in the format 'name-you-chose.serve.scilifelab.se'.
* **Permissions:** The permissions for the app. There are 3 levels of permissions you can choose from:
  - **Private:** The app can only be accessed by the user that created the app (sign in required). Please note that we only allow the permissions to be set to Private temporarily, while you are developing the app. Eventually each app should be published publicly.
  - **Project:** All members of the project where the app is located will be able to access the app (sign in required). Please note that we only allow the permissions to be set to Project temporarily, while you are developing the app. Eventually each app should be published publicly.
  - **Public:** Anyone with the URL can access the app and the app will be displayed under Public apps page.
* **App Port:** The port that the your app runs on (in case of our template it will be 8080).
* **DockerHub Image:** Name of the image on DockerHub or full url to the image on a different repository.

You can leave the other fields as default.

## Congratulations!

Congratulations, you just built and started hosting your first machine learning demo application!

Feel free to get in touch with the SciLifeLab Serve team with questions: serve@scilifelab.se.
