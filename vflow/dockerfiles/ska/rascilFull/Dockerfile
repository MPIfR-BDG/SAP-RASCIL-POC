FROM docker.io/timcornwell/rascil-full

RUN groupadd -g 1972 vflow && useradd -g 1972 -u 1972 -m vflow
USER 1972:1972
WORKDIR /home/vflow
ENV HOME=/home/vflow
 
RUN python3.6 -m pip install --user tornado==5.0.2
