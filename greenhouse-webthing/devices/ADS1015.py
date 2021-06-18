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

import Adafruit_ADS1x15
import logging
from .devices import I2Cexists

ADS1015ADDRESS = 0x48 # Alternatice address is 0x49

################################################################################
class ADS1015():

    def __init__(self):
        self.address = ADS1015ADDRESS
        if self.available():
            self.adc = Adafruit_ADS1x15.ADS1015(address=self.address)
        else:
            logging.debug("No ADS1015 found on: {}" . format(hex(self.address)))

    def available(self):
        return I2Cexists(self.address)

    def read(self, port=0):
        try:
            if self.available():
                return self.adc.read_adc(port, gain=1)
            else:
                return -1
        except: # exception if read_byte fails
            return False
################################################################################