# Select base image (can be ubuntu, python, shiny etc)
FROM python:3.11-slim

# Create user name and home directory variables. 
# The variables are later used as $USER and $HOME. 
ENV USER=username
ENV HOME=/home/$USER

# Add user to system
RUN useradd -m -u 1000 $USER

# Set working directory (this is where the code should go)
WORKDIR $HOME/app

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common

# Copy code and start script (this will place the files in home/username/)
COPY requirements.txt $HOME/app/requirements.txt
COPY main.py $HOME/app/main.py
# copy any other files that are needed for your app with the directory structure as your files expect
#COPY data/ $HOME/app/data #uncomment if you are uploading data

RUN pip install --no-cache-dir -r requirements.txt \
    && chown -R $USER:$USER $HOME \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

USER $USER
EXPOSE 7680
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "main.py"]