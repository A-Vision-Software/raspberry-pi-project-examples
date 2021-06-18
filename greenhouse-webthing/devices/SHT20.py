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

import logging
from sht20 import SHT20

SHT20ADDRESS = 0x40 # Fixed!

################################################################################
class greenhouseSHT20():

    def __init__(self):
        self.address = SHT20ADDRESS
        self.sht20 = False
        if not self.available():
            logging.debug("No SHT20 found on: {}" . format(hex(self.address)))

    def available(self):
        try:
            if (self.sht20):
                return True
            self.sht20 =  SHT20(1, resolution=SHT20.TEMP_RES_14bit)
            return True
        except:
            return False

    def temperature(self):
        try:
            if self.available():
                return self.sht20.read_temp()
            else:
                return -1
        except:
            return False

    def humidity(self):
        try:
            if self.available():
                return self.sht20.read_humid()
            else:
                return -1
        except:
            return False
################################################################################