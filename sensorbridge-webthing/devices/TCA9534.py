###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        I2C devices
#
# Created by       :        Arnold Velzel
# Created on       :        24-05-2021
#
################################################################################

import smbus2
import logging
from .devices import I2Cexists

TCA9534ADDRESS = 0x38 # Fixed!

################################################################################
class TCA9534():

    def __init__(self, I2Caddress=TCA9534ADDRESS):
        self.bus = smbus2.SMBus(1)
        self.address = I2Caddress
        self.reset()
        if not self.available():
            logging.debug("No TCA9534 found on: {}" . format(hex(self.address)))

    def available(self):
        try:
            # Read config byte
            self.bus.read_byte_data(self.address, 0x02)
            return True
        except: # exception if read_byte fails
            return False
        #return I2Cexists(self.address)

    def __del__(self):
        self.reset()
        self.bus.close()

    def reset(self):
        self.config = 0b11111111 # Define al I/O and input
        self.output = 0b00000000 # default outputs all zero
        self.polarity = 0b00000000 # default all outputs non-inverted
        self.write_config()

    def read_config(self):
        if self.available():
            self.polarity = self.bus.read_byte_data(self.address, 0x02)
            self.config = self.bus.read_byte_data(self.address, 0x03)

    def write_config(self):
        if self.available():
            self.bus.write_byte_data(self.address, 0x02, self.polarity)
            self.bus.write_byte_data(self.address, 0x03, self.config)
        
    def set_input(self, bit):
        if (self.config & (1 << bit) == 0):
            self.config = self.config | (1 << bit)
            self.write_config()

    def set_output(self, bit, inverted=None):
        if (inverted != None):
            if (inverted):
                self.polarity = self.polarity | (1 << bit)
            else:
                self.polarity = self.polarity & ~(1 << bit)

        if (self.config & (1 << bit) > 0):
            self.config = self.config & ~(1 << bit)
            self.write_config()

    def read(self, bit):
        self.set_input(bit)
        bits = 0
        if self.available():
            bits = self.bus.read_byte_data(self.address, 0x00)
        return (bits & (1 << bit)) > 0

    def write(self, bit, value):
        self.set_output(bit)
        if (value):
            self.output = self.output | (1 << bit)
        else:
            self.output = self.output & ~(1 << bit)
            
        if self.available():
            self.bus.write_byte_data(self.address, 0x01, self.output)
################################################################################
