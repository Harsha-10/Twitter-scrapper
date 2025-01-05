#!/bin/bash

# Update package lists
apt-get update

# Install required packages
apt-get install -y wget curl unzip libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

# Install OpenSSL 1.1 (if not available in repos, download and install manually)
if ! apt-get install -y libssl1.1; then
    wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl1.1/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
    dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
    apt-get install -f -y
fi

# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y

# Install Chromedriver
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

# Install Python dependencies
pip install -r requirements.txt
