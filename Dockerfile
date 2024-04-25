FROM python:3.10-buster

ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

ARG PYPI
ARG TRUSTED_HOST

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)


ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -i $PYPI --trusted-host=${TRUSTED_HOST}  -r requirements.txt


# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 8000

# Define environment variable
ENV PYTHONPATH /app

# Creates a non-root user and adds permission to access the /app folder
RUN useradd appuser && chown -R appuser /app
USER appuser
# Run app.py when the container launches
CMD ["dumb-init", "gunicorn"]
