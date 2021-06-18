#!/bin/bash

echo "updating source code"
wget https://github.com/A-Vision-Software/raspberry-pi-project-examples/archive/refs/heads/main.zip
unzip -j -o main.zip "raspberry-pi-project-examples-main/sensorbridge-webthing/*" -d .
rm main.zip

chmod 0755 install.sh
chmod 0755 update.sh

if systemctl is-active --quiet sensorbridge
then 
    echo "restarting sensorbridge service"
    sudo service sensorbridge stop
    sleep 1
    sudo service sensorbridge start
fi

echo "done..."
