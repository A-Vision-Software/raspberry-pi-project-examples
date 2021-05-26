#!/bin/bash

wget https://github.com/A-Vision-Software/raspberry-pi-project-examples/archive/refs/heads/main.zip
unzip -j -o main.zip "raspberry-pi-project-examples-main/greenhouse/*" -d .
rm main.zip

chmod 0755 install.sh
chmod 0755 update.sh

sudo service greenhouse stop
sleep 1
sudo service greenhouse start
