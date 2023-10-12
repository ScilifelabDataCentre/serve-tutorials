# Container demo 2

Demo aims:
* Demonstrate how to containerize a ML solution
* Demonstrate how to run ML training using container on HPC


## Demonstrate how to containerize a ML solution

Creating and testing the docker image locally

1. Show extended Dockerfile. Note lines:
    USER root
    requirements.txt
    installation of needed libraries

2. Build docker image using dockerfile
    `docker build -t custom-pytorch .`

3. Publish the docker image to a container repository. Login to e.g. ghcr and:
    `docker push ghcr.io/NAMESPACE/IMAGE_NAME:latest`

4. Verify that the image has been published. In this case navigate to
    https://github.com/users/sandstromviktor/packages/container/package/custom-pytorch


## Demonstrate how to run ML training using container on HPC

Instructions for running the container on Berzelius using Apptainer.

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

Clone the source code repository and view the contents.
Note that we can do this from the login node on the HPC, so we do not consume GPU allotted time.
```
git clone https://github.com/ScilifelabDataCentre/serve-tutorials.git
ls ./serve-tutorials
```

(TODO? here we could run ML training without container...)

Pull the docker image via Apptainer. This is converted to a singularity (.sif) file
```
apptainer pull custom-pytorch.sif docker://ghcr.io/sandstromviktor/custom-pytorch:latest
ls
```

Open a new terminal window

Run an interactive session on a compute node and view information about the computing resources
```
interactive --gpus=1
lscpu
nvidia-smi
```

In this interactive session, we have access to our project folder
```
pwd
cd /proj/<project-name>/solution
# cd /proj/berzelius-2023-215/solution
ls
```

In the original terminal window, view currently open sessions / running jobs
```
squeue -u <username>
```

Back in the compute terminal window, let us open a shell to the Apptainer
```
pwd
ls
apptainer shell --nv custom-pytorch.sif
# -nv enables nvidia support

pwd
ls
```

Note that the user in the container is now a non-root user. Recall that the user was root when building the image but we are not permitted to run containers as root when run on Berzelius.
```
whoami
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

Finally exit from the compute node so we do not continue to consume GPU resources
```
exit
```
