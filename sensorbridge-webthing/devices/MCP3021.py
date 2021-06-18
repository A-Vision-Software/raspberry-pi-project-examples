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

MCP3021ADDRESS = 0x4d # Fixed!

################################################################################
class MCP3021():
    
    def __init__(self, I2Caddress=MCP3021ADDRESS):
        self.bus = smbus2.SMBus(1)
        self.address = I2Caddress
        self.reset()
        if not self.available():
            logging.debug("No MCP3021 found on: {}" . format(hex(self.address)))

    def available(self):
        return I2Cexists(self.address)

    def __del__(self):
        self.reset()
        self.bus.close()

    def reset(self):
        self.config = 0

    def read(self):
        if self.available():
            data = self.bus.read_i2c_block_data(self.address, 0, 2)
            return (data[0]*256 + data[1]) >> 2

        return 0
################################################################################