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
import Adafruit_ADS1x15
from sht20 import SHT20
import time

ADS1015ADDRESS = 0x48 # Alternatice address is 0x49
SHT20ADDRESS = 0x40 # Fixed!
SHT21ADDRESS = 0x40 # Fixed!
TMP75ADDRESS = 0x4F # Fixed!
MCP3425ADDRESS = 0x68 # Fixed!

################################################################################
def I2Cexists(I2Caddress, I2Cbus=1):
    bus = smbus2.SMBus(I2Cbus) # 1 indicates /dev/i2c-1
    try:
        bus.read_byte(I2Caddress)
        bus.close()
        return True
    except: # exception if read_byte fails
        return False
################################################################################

################################################################################
class _MCP3425():
    def __init__(self):
        self.address = MCP3425ADDRESS

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



################################################################################
class _TMP75():

    def __init__(self):
        self.address = TMP75ADDRESS

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

################################################################################
class _ADS1015():

    def __init__(self):
        self.address = ADS1015ADDRESS
        if self.available():
            self.adc = Adafruit_ADS1x15.ADS1015(address=self.address)

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

################################################################################
class _SHT20():

    def __init__(self):
        self.address = SHT20ADDRESS
        self.sht20 = False

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

################################################################################
class _SHT21():

    def __init__(self):
        self.address = SHT21ADDRESS
        self.sht21 = False

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
        except: # exception if read_byte fails
            return False

    def humidity(self):
        try:
            if self.available():
                return self.sht21.read_humid()
            else:
                return -1
        except: # exception if read_byte fails
            return False
################################################################################
