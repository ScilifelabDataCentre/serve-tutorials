# Container demo 2

Demo aims:
* Demonstrate how to containerize a ML solution
* Demonstrate how to run ML training using container on HPC


## Demonstrate how to containerize a ML solution

These instructions demonstrate how to create a docker image.

1. Show the Dockerfile. Note the lines
    - `FROM pytorch/pytorch:latest`
    - `USER root`
    - and installation of additional libraries

2. Build docker image using dockerfile
    `docker build -t custom-pytorch .`

3. Publish the docker image to a container repository. Login to e.g. ghcr and:
    `docker push ghcr.io/NAMESPACE/IMAGE_NAME:latest`

4. Verify that the image has been published. In this case navigate to
    https://github.com/users/sandstromviktor/packages/container/package/custom-pytorch


## Demonstrate how to run ML training using container on HPC

These instructions cover how to run the container on Berzelius using Apptainer.

Login to Berzelius
```
ssh username@berzelius1.nsc.liu.se
# enter password
# enter 2FA verification code
```

View project information
```
projinfo
```

Navigate to our project folder and create a solution folder
```
cd /proj/<project-name>
# cd /proj/berzelius-2023-215

mkdir solution; cd solution
```

Open a new terminal window

Run an interactive session on a compute node
```
interactive --gpus=1

# We can view information about the computing resources using commands such as
lscpu
nvidia-smi
```

In this interactive session, we have access to our project folder
```
pwd
cd /proj/<project-name>/solution
# cd /proj/berzelius-2023-215/solution
```

Clone the source code repository and view the contents.
```
git clone https://github.com/ScilifelabDataCentre/serve-tutorials.git
ls ./serve-tutorials/Webinars/2023-Using-containers-on-Berzelius/
```

Attempt to setup the training without using a container and observe that we are not allowed to install the required packages.
```
pip3 install ffmpeg
# output:  error: could not create '/usr/local/lib/python3.6': Permission denied
```

Pull the docker image via Apptainer. Observe that Apptainer converts the OCI image to a singularity (.sif) file
```
apptainer version
apptainer pull custom-pytorch.sif docker://ghcr.io/sandstromviktor/custom-pytorch:latest
ls
```

Back in the compute terminal window, let us open a shell to the Apptainer
```
apptainer shell --nv custom-pytorch.sif
# -nv enables nvidia support
```

Observe that we have access to our project folder from within the image.
```
pwd
ls
```

Note that the user in the container is now a non-root user. Recall that the user was root when building the image but we are not permitted to run containers as root when run on Berzelius.
```
whoami
```

Note that we can install libraries in out container (we cannot pip install libraries on the compute node).
```
Apptainer> pip3 install ffmpeg
```

Navigate to the code folder and extract the dataset
```
cd ./serve-tutorials/Webinars/2023-Using-containers-on-Berzelius/cancer-cell-classification

# Note that the dataset is not included in the tutorials repository.
unzip -q /proj/berzelius-2023-215/solution/data.zip -d .

ls ./data
```

Run model training on Berzelius using the container
```
cd ./02-local-scripts
ls
python3 train.py --epochs=2
```

The training will take some time. In the meantime, we can explore how to view currently open sessions / running jobs. In the original terminal window, execute: 
```
squeue -u <username>
```

Note: We *can* create a python virtual environment and install our libraries there. But this requires extra work and is not always guaranteed to work because of underlying OS and libraries.

Using a containerized solution can also improve efficiency in performing work and moving back and forth between the HPC and local work. Changes made in the container can be pushed to an image repository and pulled down to other local machines. 

When model training has completed, note that the model was saved to a pytorch archive file and the metrics and training graphs were created.
```
ls ./models
cat ./output/CNN/metrics.txt
```

Finally exit from the container and exit the compute node so we do not continue to consume GPU resources
```
exit
exit
```
