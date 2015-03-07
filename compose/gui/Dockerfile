FROM node:0.12

RUN apt-get update

WORKDIR /opt/dc-gui

# npm deps
ADD ./package.json /opt/dc-gui/package.json
RUN cd /opt/dc-gui && npm install
RUN mv /opt/dc-gui/node_modules /opt/

# Server
ENV PATH /opt/node_modules/.bin/:$PATH
