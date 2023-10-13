#!/bin/bash

version=$1

cd /tmp/
wget https://www.python.org/ftp/python/"$version"/Python-"$version".tgz
tar xzf Python-"$version".tgz
cd Python-"$version"

sudo ./configure --prefix=/usr/local/python/"$version"/ --enable-optimizations
sudo make -j "$(nproc)"
sudo make altinstall
sudo rm /tmp/Python-"$version".tgz
