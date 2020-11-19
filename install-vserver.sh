#!/usr/bin/env sh

# Install docker from repository

sudo apt update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Install miniconda for root

MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

sudo su
mkdir /app
cd /app || exit



curl -o miniconda.sh $MINICONDA_URL
sh ./miniconda.sh
