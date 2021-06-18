#!/bin/bash

echo "updating source code"
wget https://github.com/A-Vision-Software/raspberry-pi-project-examples/archive/refs/heads/main.zip
unzip -j -o main.zip "raspberry-pi-project-examples-main/powercontrol-webthing/*" -d .
rm main.zip

chmod 0755 install.sh
chmod 0755 update.sh

if systemctl is-active --quiet powercontrol
then 
    echo "restarting powercontrol service"
    sudo service powercontrol stop
    sleep 1
    sudo service powercontrol start
fi

echo "done..."
