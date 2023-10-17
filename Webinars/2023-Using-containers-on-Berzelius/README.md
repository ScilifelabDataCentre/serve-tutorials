# Using containers to simplify ML training on Berzelius and other supercomputers: beginner-friendly introduction

A webinar event held on October 19. 2023 by the [SciLifeLab Data Centre](https://www.scilifelab.se/data/)

This webinar is part of an event series arranged by the SciLifeLab Data Centre focused on tools for AI/ML research in life sciences.

## Abstract

A common approach to train machine learning models is to first create a prototype using a small dataset on a local machine to verify that it works and thereafter use a large scale compute infrastructure such as Berzelius for the full-scale training. One of the challenges with this approach however is incompatible systems in terms of differences in available software packages, versions, etc. An effective way to solve this issue is to use a container solution. Using a container environment allows a highly portable workflow and reproducible results between systems as diverse as a laptop, Berzelius or EuroHPC resources such as LUMI for instance. During this beginner-friendly event, we will introduce and demonstrate how to work with containers on Berzelius (Apptainer and Enroot) using an example from life sciences, starting from raw data and finishing with a trained model. During the Q&A session, the Berzelius life science support team will answer your questions.

## Learning outcomes and pre-requisities

This webinar and its demos assume that the reader is familiar with Python, machine learning, Jupyter Lab notebooks, and the Linux OS. An introduction to docker, containers, and HPC is provided in the presentation.

## Contents

This webinar folder contains the following items:
- the presentation file presentation.pdf
- a machine learning task located in flowers-classification
- container demos in the container-demo-* folders including instructions


## Overview of the machine learning task

The sample ML task is to predict the correct flower category from an image. The flowers are commonly occuring flowers in United Kingdom such as water lily and petunia.

For information about the dataset used, see 
https://www.robots.ox.ac.uk/~vgg/data/flowers/102/

The database was used in:

Nilsback, M-E. and Zisserman, A. Automated flower classification over a large number of classes.
Proceedings of the Indian Conference on Computer Vision, Graphics and Image Processing (2008) 
http://www.robots.ox.ac.uk/~vgg/publications/papers/nilsback08.{pdf,ps.gz}.

The flowers-classification directory is structured into two parts according to the presentation to demonstrate the different approaches and steps presented.

- A Jupyter Lab notebook containing a presentation of the ML problem and an initial solution working on a local machine
- A set of python scripts for running the ML training locally and on HPC

## Instructions

These instructions guide the user in following the demos from the presentation.

Clone this repository

    git clone https://github.com/ScilifelabDataCentre/serve-tutorials.git

Open the folder /serve-tutorials/Webinars/2023-Using-containers-on-Berzelius/

## Setup and system requirements

The instructions assume the Linux OS but should work also on MacOS and Windows with minor modifications.

To get started, create a virtual environment and install the needed libraries from the requirements file. Open a terminal and from the repository root directory (/serve-tutorials), execute:

    cd Webinars/2023-Using-containers-on-Berzelius/flowers-classification
    python3 -m venv .venv01
    source ./.venv01/bin/activate

Upgrade pip and install the required libraries

    python3 -m pip install --upgrade pip
    pip3 install -r requirements.txt

    # For use of Jupyter Lab notebooks
    pip3 install ipykernel
    # Required for select correct jupyter kernel in vscode
    python3 -m ipykernel install --user --name=.venv01

Install PyTorch. If using CPU:

    python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

If using GPU CUDA:

    pip3 install torch torchvision torchaudio


### Running the notebook

The notebook introduces the ML problem and an initial deep learning solution. Open the notebook /flowers-classification/local-solution-notebook.ipynb and either simply read the cells to understand the problem, code and outputs or execute the notebook cells to see the solution in action.

Before executing the cells, select the kernel from the virtual environment previously created, i.e.

    "Webinars/2023-Using-containers-on-Berzelius/flowers-classification/.venv01/bin/python3"


## Running the python scripts

The solution from the notebook is also implemented as a set of python scripts for model training and evaluation. These scripts can be executed on a local machine to see the solution in action. They form the basis of the next step: containarizing the solution in preparation of running on an HPC such as Berzelius. The main python script of interest is *train.py*.

For example in order to train the model for 2 epochs, the user should run:

    cd ./02-scripts
    python3 train.py --epochs=2


## Container demo

Now you are ready to containerize the solution and run this on an HPC. For this see the instructions in the /container-demo-2/README.md file
