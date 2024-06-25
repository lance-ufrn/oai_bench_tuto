#!/bin/bash

# Work directory path is the current directory
WORK_DIR=`pwd`

# Start with update 
sudo apt-get update

## Install dependencies
sudo apt-get install ca-certificates -y
sudo apt-get install curl -y
sudo apt-get install gnupg -y
sudo apt-get install lsb-release -y

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Defining specific version of paper
VERSION_STRING=5:24.0.7-1~ubuntu.20.04~focal
sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin=2.21.0-1~ubuntu.20.04~focal -y

# Enabling current user to run docker commands
sudo usermod -aG docker $USER

# UHD tools to build the driver
sudo apt-get install autoconf automake build-essential ccache cmake cpufrequtils doxygen ethtool g++ git inetutils-tools libboost-all-dev libncurses5 libncurses5-dev libusb-1.0-0 libusb-1.0-0-dev libusb-dev python3-dev python3-mako python3-numpy python3-requests python3-scipy python3-setuptools python3-ruamel.yaml -y

# Install libuhd v4.4.0.0
sudo add-apt-repository ppa:ettusresearch/uhd
sudo apt-get update
sudo apt install libuhd4.4.0 -y

# Get UHD code to build
git clone https://github.com/EttusResearch/uhd.git ~/uhd
cd ~/uhd/host/
# Set the drivers version
git checkout v4.4.0.0
cmake ./
sudo make install

## Pulling the images from Docker Hub
sudo docker pull oaisoftwarealliance/oai-amf:v1.5.0
sudo docker pull oaisoftwarealliance/oai-nrf:v1.5.0
sudo docker pull oaisoftwarealliance/oai-smf:v1.5.0
sudo docker pull oaisoftwarealliance/oai-udr:v1.5.0
sudo docker pull oaisoftwarealliance/oai-udm:v1.5.0
sudo docker pull oaisoftwarealliance/oai-ausf:v1.5.0
sudo docker pull oaisoftwarealliance/oai-spgwu-tiny:v1.5.0
sudo docker pull oaisoftwarealliance/trf-gen-cn5g:latest

## Tag Docker Images
sudo docker image tag oaisoftwarealliance/trf-gen-cn5g:latest trf-gen-cn5g:latest
sudo docker image tag oaisoftwarealliance/oai-amf:v1.5.0 oai-amf:v1.5.0
sudo docker image tag oaisoftwarealliance/oai-nrf:v1.5.0 oai-nrf:v1.5.0
sudo docker image tag oaisoftwarealliance/oai-smf:v1.5.0 oai-smf:v1.5.0
sudo docker image tag oaisoftwarealliance/oai-udr:v1.5.0 oai-udr:v1.5.0
sudo docker image tag oaisoftwarealliance/oai-udm:v1.5.0 oai-udm:v1.5.0
sudo docker image tag oaisoftwarealliance/oai-ausf:v1.5.0 oai-ausf:v1.5.0
sudo docker image tag oaisoftwarealliance/oai-spgwu-tiny:v1.5.0 oai-spgwu-tiny:v1.5.0