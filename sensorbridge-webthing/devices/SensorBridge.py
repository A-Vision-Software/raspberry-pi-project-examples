###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        A-Vision Sensor bridge
#
# Created by       :        Arnold Velzel
# Created on       :        01-06-2021
#
###############################################################################

import smbus2
import logging
from .devices import I2Cexists
from .TCA9534 import TCA9534
from .MCP3021 import MCP3021

SENSORBRIDGEADDRESS = 0x71 # Range 0x70 - 0x77

class SensorBridge():
    
    def __init__(self, I2Caddress=SENSORBRIDGEADDRESS):
        self.bus = smbus2.SMBus(1)
        self.address = I2Caddress
        self.analog_channel = 0
        self.reset()
        self.digital = TCA9534()
        self.analog = MCP3021()
        if (self.available()):
            logging.debug("SensorBridge status: {}" . format(bin(self.bus.read_byte(self.address))))
        else:
            logging.debug("No SensorBridge found on: {}" . format(hex(self.address)))

    def available(self):
        return I2Cexists(self.address)

    def __del__(self):
        del self.digital
        del self.analog
        self.bus.write_byte(self.address, 0x00)
        self.bus.close()
        logging.debug("SensorBridge closed")

    def read_analog(self, channel):
        logging.debug("SensorBridge read analog: {}" . format(channel))
        self.select_analog(channel)
        return self.analog.read() * 100  / 1024

    def read_digital(self, bit):
        logging.debug("SensorBridge read digital: {}" . format(bit))
        return self.digital.read(bit)

    def write_digital(self, bit, value):
        logging.debug("SensorBridge write digital: {} => {}" . format(bit, str(value)))
        return self.digital.write(bit, value)

    def reset(self):
        self.select_analog(1)

    def select_analog(self, channel):
        self.analog_channel = channel
        if (self.available()):
            if (channel == 1):
                self.bus.write_byte(self.address, 0b10000011)
            if (channel == 2):
                self.bus.write_byte(self.address, 0b10000101)
