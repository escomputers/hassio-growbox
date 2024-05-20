#!/bin/bash

# Install build requirements
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget -y

version=$1

# Extracting major and minor version components
major_minor_version="${version%.*}"

cd /tmp/
wget https://www.python.org/ftp/python/"$version"/Python-"$version".tgz
tar -xf Python-"$version".tgz
cd Python-"$version"

./configure --enable-optimizations
sudo make install
sudo make altinstall  # set as default version from now on

# Link "python" to the new installation 
sudo ln -s /usr/local/bin/python3 /usr/bin/python

# Clean up
sudo rm /tmp/Python-"$version".tgz

# Verify installation
echo "python3 -V output:"
python3 -V

echo "python -V output:"
python -V
