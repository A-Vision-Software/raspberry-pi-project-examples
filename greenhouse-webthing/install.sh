#!/bin/bash

echo "installing I2C support"
pip3 install smbus2
echo "installing GPIO support"
pip3 install rpi.gpio
pip3 install gpiozero
echo "installing WebThings framework"
pip3 install webthing
echo "installing SHT20 support"
pip3 install sht20
echo "installing ADS1015 support"
pip3 install adafruit-ads1x15

echo "done..."