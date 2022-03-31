FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

ARG USER_ID
ARG GID
ARG PROJECT_DIR=/app
ARG APP_ROOT=/app/app

# Set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Taipei
ENV PATH=/home/docker:/home/docker/.local/bin:${PATH}

# Create user
RUN groupadd -g $GID -f docker-users && \
    useradd -m --no-log-init -s /bin/bash -u $USER_ID -g $GID docker && \
    echo "docker:docker" | chpasswd && \
    adduser docker sudo

# Set timezone and install packages 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get --allow-releaseinfo-change update && \
    apt-get install -y --no-install-recommends sudo && \
    apt-get clean && \
    apt-get autoremove

# Set locale
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

WORKDIR $PROJECT_DIR

# Copy code, install required packages, create directories and change permission
COPY . .

WORKDIR $PROJECT_DIR
RUN pip install pipenv && \
    pipenv install --system --deploy && \
    chown -R $USER_ID:$GID $PROJECT_DIR

# Use non-root user to start service
WORKDIR ${APP_ROOT}
USER docker
