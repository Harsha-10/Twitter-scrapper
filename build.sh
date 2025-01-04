#!/bin/bash
# Install dependencies and Chrome
apt-get update && apt-get install -y wget unzip

# Download and install Chrome
wget -q -O google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Download ChromeDriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
wget -q -O chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_VERSION%.*}/chromedriver_linux64.zip
unzip chromedriver.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/
