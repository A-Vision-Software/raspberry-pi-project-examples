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

###############################################################################
def I2Cexists(I2Caddress, I2Cbus=1):
    bus = smbus2.SMBus(I2Cbus) # 1 indicates /dev/i2c-1
    try:
        bus.read_byte(I2Caddress)
        bus.close()
        return True
    except: # exception if read_byte fails
        return False
################################################################################
