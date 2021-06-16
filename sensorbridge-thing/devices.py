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

TMP75ADDRESS = 0x4F # Fixed!
MCP3425ADDRESS = 0x68 # Fixed!
SENSORBRIDGEADDRESS = 0x71 # Range 0x70 - 0x77

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



################################################################################
class _TMP75():

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

################################################################################
class MCP3021():
    
    def __init__(self, I2Caddress=0x4d):
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


################################################################################
class TCA9534():

    def __init__(self, I2Caddress=0x38):
        self.bus = smbus2.SMBus(1)
        self.address = I2Caddress
        self.reset()
        if not self.available():
            logging.debug("No TCA9534 found on: {}" . format(hex(self.address)))

    def available(self):
        return I2Cexists(self.address)

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
