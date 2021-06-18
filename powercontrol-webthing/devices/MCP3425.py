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
import time
import logging
from .devices import I2Cexists

MCP3425ADDRESS = 0x68 # Fixed!

################################################################################
class MCP3425():
    def __init__(self):
        self.address = MCP3425ADDRESS
        if not self.available():
            logging.debug("No MCP3425 found on: {}" . format(hex(self.address)))

    def available(self):
        return I2Cexists(self.address)

    def read(self):
        bus = smbus2.SMBus(1) # 1 indicates /dev/i2c-1
        try:
            bus.write_byte(self.address, 0x10)
            time.sleep(0.1)
            data = bus.read_i2c_block_data(self.address, 0x00, 2)
            raw_adc = (data[0] & 0x0F) * 256 + data[1]
            if raw_adc > 2047 :
                raw_adc -= 4095
            bus.close()
            return raw_adc
        except: # exception if read_byte fails
            return False
################################################################################
