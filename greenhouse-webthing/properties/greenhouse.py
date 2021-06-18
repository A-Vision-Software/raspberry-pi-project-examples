###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        Greenhouse properties
#
# Created by       :        Arnold Velzel
# Created on       :        24-05-2021
#
################################################################################

import logging
import tornado.ioloop
from time import sleep
from gpiozero import DigitalOutputDevice
from webthing import (Property, Value)
from devices.ADS1015 import ADS1015
from devices.SHT20 import greenhouseSHT20

from config import config
_config = config.Config('greenhouse')

################################################################################
class AnalogInput_property(Property):
    """Single analog input."""

    def __init__(self, theThing, propertyName='', enablePin=0, analogPin=0):
        self.adc = ADS1015()
        self.available = self.adc.available()
        if not self.available:
            logging.warning('ADS1015 device not found')
            propertyName = 'FAKE: ' + propertyName

        self.analogPin = analogPin
        self.enable = DigitalOutputDevice(enablePin, active_high=False)
        self.inputValue = Value(0.0)
        Property.__init__(
            self,
            thing=theThing,
            name=propertyName,
            value=self.inputValue,
            metadata={
                '@type': 'LevelProperty',
                'title': propertyName,
                'type': 'number',
                'minimum': 0,
                'maximum': 100,
                'unit': 'percent',
                'readOnly': True,
                'description': 'Analog input ' + propertyName
            }
        )
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update,
            (int(_config.setting('SLOWUPDATEINTERVAL')) + analogPin*2) * 1000,
            0.2
        )
        self.timer.start()

    def update(self):
        self.enable.on()
        sleep(1)
        if self.adc:
            value = self.adc.read(self.analogPin) / 2048 * 100
        else:
            value = 0
        self.enable.off()
        self.inputValue.notify_of_external_update(value)

    def cancel(self):
        self.timer.stop()
################################################################################

################################################################################
class TemperatureHumidity_property(Property):
    """Temperature sensor"""

    def __init__(self, theThing, propertyName='', parameter=''):
        self.parameter = parameter
        self.sht = greenhouseSHT20()
        self.available = self.sht.available()
        if not self.available:
            logging.warning('SHT20 device not found')
            propertyName = 'FAKE: ' + propertyName
        self.inputValue = Value(0.0)
        propertyType = 'LevelProperty'
        if self.parameter == 'temperature':
            propertyType = 'TemperatureProperty'
            propertyUnit = '°C'
            propertyMinimum = -40
            propertyMaximum = 125
        if self.parameter == 'humidity':
            propertyType = 'HumidityProperty'
            propertyUnit = 'percent'
            propertyMinimum = 0
            propertyMaximum = 100
        Property.__init__(
            self,
            thing=theThing,
            name=propertyName,
            value=self.inputValue,
            metadata={
                '@type': propertyType,
                'title': propertyName,
                'type': 'number',
                'minimum': propertyMinimum,
                'maximum': propertyMaximum,
                'unit': propertyUnit,
                'readOnly': True,
                'description': parameter +' ' + propertyName
            }
        )
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update,
            int(_config.setting('FASTUPDATEINTERVAL')) * 1000
        )
        self.timer.start()

    def update(self):
        value = 0
        if self.available:
            if self.parameter == 'temperature':
                value = self.sht.temperature()
            if self.parameter == 'humidity':
                value = self.sht.humidity()
        self.inputValue.notify_of_external_update(value)

    def cancel(self):
        self.timer.stop()
################################################################################