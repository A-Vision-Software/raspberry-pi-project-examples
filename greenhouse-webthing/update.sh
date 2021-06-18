#!/bin/bash

echo "updating source code"
wget https://github.com/A-Vision-Software/raspberry-pi-project-examples/archive/refs/heads/main.zip
unzip -o main.zip "raspberry-pi-project-examples-main/greenhouse-webthing/*" -d .
rm main.zip
mv raspberry-pi-project-examples-main/greenhouse-webthing/* .
rm -r raspberry-pi-project-examples-main/

chmod 0755 install.sh
chmod 0755 update.sh

if systemctl is-active --quiet greenhouse
then 
    echo "restarting greenhouse service"
    sudo service greenhouse stop
    sleep 1
    sudo service greenhouse start
fi

echo "done..."
