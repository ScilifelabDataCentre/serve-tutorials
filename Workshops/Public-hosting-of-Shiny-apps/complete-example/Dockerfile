# Base image
FROM rocker/shiny:4.4.1

# General updates
#RUN apt-get update && \
#    apt-get upgrade -y && \
#    apt-get install -y git libxml2-dev libmagick++-dev libssl-dev libharfbuzz-dev libfribidi-dev && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

# Install the required packages
# Recreate the R environment using renv package
#RUN Rscript -e 'install.packages(c("renv"))'
#COPY /renv.lock /srv/shiny-server/renv.lock
#RUN Rscript -e 'setwd("/srv/shiny-server/");renv::restore();'

# Install packages directly instead of using renv snapshot
RUN Rscript -e 'install.packages(c("dplyr", "ggplot2", "scales", "readr"))'

# Copy the app files (scripts, data, etc.)
RUN rm -rf /srv/shiny-server/*
COPY /app/ /srv/shiny-server/

# Ensure that the expected default user is present in the container for cases when it is used to host the app over the web
RUN if id shiny &>/dev/null && [ "$(id -u shiny)" -ne 999 ]; then \
        userdel -r shiny; \
        id -u 999 &>/dev/null && userdel -r "$(id -un 999)"; \
    fi; \
    useradd -u 999 -m -s /bin/bash shiny; \
    chown -R shiny:shiny /srv/shiny-server/ /var/lib/shiny-server/ /var/log/shiny-server/

# Other settings
USER shiny
EXPOSE 3838

CMD ["/usr/bin/shiny-server"]