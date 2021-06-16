#!/bin/bash

echo "installing I2C support"
pip3 install smbus2
echo "installing GPIO support"
pip3 install rpi.gpio
pip3 install gpiozero
echo "installing WebThings framework"
pip3 install webthing 

echo "done..."