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
2. Copy test.txt.
3. Build and run container
4. Show that vim and test.txt are part of the container
