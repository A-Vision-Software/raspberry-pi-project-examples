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

TMP75ADDRESS = 0x4F # Fixed!

################################################################################
class TMP75():

    def __init__(self):
        self.address = TMP75ADDRESS
        if not self.available():
            logging.debug("No TMP75 found on: {}" . format(hex(self.address)))

    def available(self):
        return I2Cexists(self.address)

    def read(self):
        bus = smbus2.SMBus(1) # 1 indicates /dev/i2c-1
        try:
            config = bus.read_byte_data(self.address, 0x01)
            resolution = 12  # allowed values are: 9,10,11,12
            config &= ~0x60  # clear bits 5,6
            config |= (resolution - 9) << 5  # set bits 5,6
            bus.write_byte_data(self.address, 0x01, config)
            time.sleep(0.1)
            data = bus.read_i2c_block_data(self.address, 0x00, 2)
            bus.close()
            return (data[0] * 256 + data[1]) / 16 / 16
        except: # exception if read_byte fails
            return False
################################################################################