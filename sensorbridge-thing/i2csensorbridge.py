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
import devices

class SensorBridge():
    
    def __init__(self, I2Caddress=0x70):
        self.bus = smbus2.SMBus(1)
        self.address = I2Caddress
        self.analog_channel = 0
        self.reset()
        self.digital = devices.TCA9534()
        self.analog = devices.MCP3021()
        if (self.available()):
            logging.debug("SensorBridge status: {}" . format(bin(self.bus.read_byte(self.address))))

    def available(self):
        return devices.I2Cexists(self.address)

    def __del__(self):
        del self.digital
        del self.analog
        self.bus.write_byte(self.address, 0x00)
        self.bus.close()
        logging.debug("SensorBridge closed")

    def read_analog(self, channel):
        logging.debug("SensorBridge read analog: {}", format(channel))
        self.select_analog(channel)
        return self.analog.read() * 100  / 1024

    def read_digital(self, bit):
        logging.debug("SensorBridge read digital: {}", format(bit))
        return self.digital.read(bit)

    def write_digital(self, bit, value):
        logging.debug("SensorBridge write digital: {} => {}", format(bit, value))
        return self.digital.write(bit, value)

    def reset(self):
        self.select_analog(1)

    def select_analog(self, channel):
        self.analog_channel = channel
        if (channel == 1):
            self.bus.write_byte(self.address, 0b10000011)
        if (channel == 2):
            self.bus.write_byte(self.address, 0b10000101)

