# Using containers to simplify ML training on Berzelius and other supercomputers: beginner-friendly introduction

A webinar event October 19. 2023

https://www.scilifelab.se/event/using-containers-berzelius/

## Abstract

A common approach to train machine learning models is to first create a prototype using a small dataset on a local machine to verify that it works and thereafter use a large scale compute infrastructure such as Berzelius for the full-scale training. One of the challenges with this approach however is incompatible systems in terms of differences in available software packages, versions, etc. An effective way to solve this issue is to use a container solution. Using a container environment allows a highly portable workflow and reproducible results between systems as diverse as a laptop, Berzelius or EuroHPC resources such as LUMI for instance. During this beginner-friendly event, we will introduce and demonstrate how to work with containers on Berzelius (Apptainer and Enroot) using an example from life sciences, starting from raw data and finishing with a trained model. During the Q&A session, the Berzelius life science support team will answer your questions.

## Learning outcomes and pre-requisities

TODO:

This webinar and its demos assume that the reader is familiar with Python, machine learning, Jupyter Lab notebooks, and the Linux OS. An introduction to docker, containers, and HPC is provided in the presentation.


## Contents

This webinar folder contains the following items:
- the presentation file presentation.pdf
- a machine learning problem located in /cancer-cell-classification


## Overview of the machine learning problem

The ML problem deals with the classification of oral cancer cells. It is based on the Kaggle challange ["Cancer Cell Challange"](https://www.kaggle.com/competitions/cancer-cell-challange/) and the github repository https://github.com/JoLinden/dl4ia-challenge

The original dataset has been reduced to 10% of the original to speed up downloads and executions.

The cancer-cell-classification directory is structured in 4 parts according to the presentation to demonstrate the different approaches and steps presented.

- A Jupyter Lab notebook containing a presentation of the ML problem and an initial solution working on a local machine
- A set of python scripts for running the ML training locally
- A set of files that containerize the solution for HPC clusters
- A dataset located in /cancer-cell-classification/data


## Instructions

These instructions guide the user in following the demos from the presentation.

Clone this repository

    git clone https://github.com/ScilifelabDataCentre/serve-tutorials.git

Open the folder /serve-tutorials/Webinars/2023-Using-containers-on-Berzelius/

## Setup and system requirements

The instructions assume the Linux OS. To get started, create a virtual environment and install the needed libraries from the requirements file. Open a terminal and from the repository root directory, execute:

    cd Webinars/2023-Using-containers-on-Berzelius/cancer-cell-classification

Create and activate a python virtual environment

    python3 -m venv .venv01
    source ./.venv01/bin/activate

Upgrade pip and install the required libraries

    python3 -m pip install --upgrade pip
    pip3 install -r requirements.txt

    # Required for select correct jupyter kernel in vscode
    python3 -m ipykernel install --user --name=.venv01

Install PyTorch. If using CPU:

    python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

If using GPU CUDA:

    pip3 install torch torchvision torchaudio


### Running the notebook

The notebook introduces the ML problem and an initial deep learning solution. Open the notebook /cancer-cell-classification/local-solution-notebook.ipynb and either simply read the cells to understand the problem, code and outputs or execute the notebook cells to see the solution in action.

Before executing the cells, select the kernel from the virtual environment previously created, i.e.

    "Webinars/2023-Using-containers-on-Berzelius/cancer-cell-classification/cancer-cell-classification/.venv01/bin/python3"


## Running the python scripts

The solution from the notebook is also implemented as a set of python scripts that train and evaluate the trained model. These scripts can be executed on a local machine to see the solution in action. They form the basis of the next step: containarizing the solution in preparation of running on an HPC such as Berzelius. The python scripts include:

- train.py
- test.py

To run model training:

    python3 train.py --model=ConvolutionalClassification --epochs=2


## Creating and testing the docker image locally


## Moving to the HPC

Instructions for running the container on Berzelius using Apptainer.


