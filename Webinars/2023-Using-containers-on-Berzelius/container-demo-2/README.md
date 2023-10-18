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

Open a new terminal window

Navigate to our project folder and create a solution folder
```
cd /proj/<project-name>
# cd /proj/berzelius-2023-215

mkdir solution; cd solution
```

Clone the source code repository and view the contents.
```
git clone https://github.com/ScilifelabDataCentre/serve-tutorials.git

cd ./serve-tutorials/Webinars/2023-Using-containers-on-Berzelius/
```

Run an interactive session on a compute node. Here we request 2 GPUs with default settings.
```
interactive --gpus=2

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

Let us see what happens if we attempt to train our model outside of a container. 
```
cd ./serve-tutorials/Webinars/2023-Using-containers-on-Berzelius/flowers-classification/02-scripts/
python3 train.py --epochs=1
# observe error: "ModuleNotFoundError: No module named 'matplotlib'"

# Attempt to install the missing python library
pip3 install matplotlib
# observe error: "PermissionError: [Errno 13] Permission denied"
```

Pull the docker image via Apptainer. Observe that Apptainer converts the OCI image to a singularity (.sif) file
```
apptainer version
apptainer pull custom-pytorch.sif docker://ghcr.io/sandstromviktor/custom-pytorch:latest
ls
```

Open a shell to the container using Apptainer
```
apptainer shell --nv custom-pytorch.sif
# -nv enables nvidia support
```

Observe that we have access to our project folder from within the image.
```
pwd
ls
```

We can also check the version of python that is available in the container and note that it may be different than the version of python that is available on the compute node. 
```
python3 -V
```

Note that the user in the container is now a non-root user. Recall that the user was root when building the image but we are not permitted to run containers as root when run on Berzelius.
```
whoami
```

Note that we can install libraries in our container (we cannot pip install libraries on the compute node).
```
Apptainer> pip3 install ffmpeg
```

Now we are ready to train our ML model. We should already be in the correct scripts folder, so simple run model training on Berzelius using the container:
```
python3 train.py --epochs=10 --batch_size=64 --lr=0.0001 --n_cpu=32 --validate_steps=200
# this training scenario will take about 2 minutes
# the same training on a typical notebook CPU will take about 1 hour
```

The training will take some time. In the meantime, we can explore how to view currently open sessions / running jobs. In the original terminal window, execute squeue and note the jobid: 
```
squeue -u <username>
```

We can login to the compute node of our training job and monitor the GPU consumption:
```
jobsh -j $jobid
nvidia-smi
```

When model training has completed, it will display the final validation accuracy:
```
On epoch 10
  Evaluating model on step 900
  Epoch: 10/10...  Training Loss: 0.1126 Validation Loss: 0.7596 Validation Accuracy: 80.7559
Training complete. Training duration 0:01:29.179998
```

We observe that this sample task took only 4.5 minutes to train for 10 epochs using a single GPU on Berzelius. The same training on a typical CPU notebook will of course vary but took us about 50 minutes for 10 epochs.

Note that the model was saved to a pytorch archive file and the metrics and training graphs were created.
```
ls ./models/
ls ./output/vgg19/
```

Note: We *can* create a python virtual environment and install our libraries there. But this requires extra work and is not always guaranteed to work because of underlying OS and libraries.

Using a containerized solution can also improve efficiency in performing work and moving back and forth between the HPC and local work. Changes made in the container can be pushed to an image repository and pulled down to other local machines.

Finally exit from the container and exit the compute node so we do not continue to consume GPU resources
```
exit
exit
```

We should no longer have an open session or compute resources reserved:
```
squeue -u <username>
```

We can now view the remaining GPU hours in our project:
```
projinfo
```
