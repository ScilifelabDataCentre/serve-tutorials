# Demo 1

## Show examples of OS
1. Show computer os `cat /etc/os-release`
2. Start Alpine container `docker run --rm -it alpine:3.18`. Show `cat /etc/os-release`
3. Start ubuntu container `docker run --rm -it ubuntu:20.04`. Show same

## Show examples of containers being "fixed"
1. In ubuntu container, run `apt update`, `apt install vim`. 
2. Use vim to create file `vim test.txt`. Write something in the file. save `wq`
3. Show file using `ls`.
4. Stop container and start again. Show that `vim` and `text.txt` is gone. 

## Show examples of Dockerfile
1. Create Dockerfile from ubuntu 20.04, run update and install vim.
2. Build and run container
3. Show that vim is a part of the container

## Show examples of prebuild containers by other teams
1. Show python version on local machine
2. run `python3` and then `import torch`. Show that it does not work
3. Start container `docker run --rm -it pytorch/pytorch:latest`
4. run `python3` and then `import torch`. Show that it does indeed work

## Show pytorch container on berzelius
1. From login node, start interactive session `interactive --gpus=1`
2. Pull image from docker hub `apptainer pull pytorch.sif docker://pytorch/pytorch:latest`
3. Start container `apptainer shell --nv pytorch.sif`
4. run `python3` and then `import torch`. Show that it does indeed work
5. after import, run `torch.cuda.is_available()` to check if GPU can be accessed
