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

SHT21ADDRESS = 0x40 # Fixed!

################################################################################
class greenhouseSHT21():

    def __init__(self):
        self.address = SHT21ADDRESS
        self.sht21 = False
        if not self.available():
            logging.debug("No SHT21 found on: {}" . format(hex(self.address)))

    def available(self):
        try:
            if (self.sht21):
                return True
            self.sht21 =  SHT20(1, resolution=SHT20.TEMP_RES_14bit)
            return True
        except:
            return False

    def temperature(self):
        try:
            if self.available():
                return self.sht21.read_temp()
            else:
                return -1
        except:
            return False

    def humidity(self):
        try:
            if self.available():
                return self.sht21.read_humid()
            else:
                return -1
        except:
            return False
################################################################################