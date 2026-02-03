# Select base image (can be ubuntu, python, shiny etc)
FROM python:3.12-slim

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
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . $HOME/app/
RUN pip install mkdocs-material

RUN chmod +x start-script.sh \
    && chown -R $USER:$USER $HOME \
    && rm -rf /var/lib/apt/lists/*

USER $USER
EXPOSE 8000

ENTRYPOINT ["./start-script.sh"]