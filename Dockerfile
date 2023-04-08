FROM python:3.9-buster
LABEL maintainer="mickael@papamica.com"
LABEL org.opencontainers.image.source=https://github.com/PAPAMICA/OpenCraft.cloud

WORKDIR /app
COPY diagrams-0.18.0.tar.gz /app/diagrams-0.18.0.tar.gz
COPY app.py /app/app.py
COPY docker_api.py /app/docker_api.py
COPY openstack_api.py /app/openstack_api.py 
COPY requirements.txt /app/requirements.txt
COPY img/ /app/img/

RUN chmod +x /app/*.py &&\
    apt update && apt install -y  graphviz &&\
    pip3 install /app/diagrams-0.18.0.tar.gz &&\
    pip3 install -r /app/requirements.txt