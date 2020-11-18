#!/bin/bash

apt-get update
apt-get install build-essential python3-dev python3-pip -y
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
python3 setup.py install
cd ~
pip3 install -r /home/debian/Wearable-Software/Firmware/src/requirements3.txt

