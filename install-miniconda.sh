#!/usr/bin/env sh

# Install miniconda for root

MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

sudo su
mkdir /app
cd /app || exit

curl -o miniconda.sh $MINICONDA_URL
sh ./miniconda.sh

