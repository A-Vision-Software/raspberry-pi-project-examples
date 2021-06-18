################################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        SensorBridge properties
#
# Created by       :        Arnold Velzel
# Created on       :        23-05-2021
#
################################################################################

import logging
import tornado.ioloop
from time import sleep
from webthing import (Property, Value)
from devices.SensorBridge import SensorBridge

from config import config
_config = config.Config('sensorbridge')
SENSORBRIDGEADDRESS = int(_config.parameter('i2c.SENSORBRIDGEADDRESS'))

################################################################################
class DigitalOutput_property(Property):
    """Single digital output."""

    def __init__(self, theThing, propertyName='', outputPin=0):
        self.outputPin = outputPin
        self.outputValue = Value(0.0, lambda v: self.setOutput(v))
        if (theThing.bridge):
            self.bridge = theThing.bridge
        else:
            self.bridge = SensorBridge(SENSORBRIDGEADDRESS)
        self.setOutput(0)
        Property.__init__(
            self,
            thing=theThing,
            name=propertyName,
            value=self.outputValue,
            metadata={
                '@type': 'OnOffProperty',
                'title': propertyName,
                'type': 'boolean',
                'description': 'Digital output ' + propertyName
            }
        )

    def setOutput(self, v):
        if (v):
            logging.debug('Set pin ON')
            self.bridge.write_digital(self.outputPin, True)
        else:
            logging.debug('Set pin OFF')
            self.bridge.write_digital(self.outputPin, False)
################################################################################

################################################################################
class DigitalInput_property(Property):
    """Single digital input."""

    def __init__(self, theThing, propertyName='', inputPin=0):
        self.inputPin = inputPin
        self.inputValue = Value(0.0)
        if (theThing.bridge):
            self.bridge = theThing.bridge
        else:
            self.bridge = SensorBridge(SENSORBRIDGEADDRESS)
        Property.__init__(
            self,
            thing=theThing,
            name=propertyName,
            value=self.inputValue,
            metadata={
                '@type': 'OnOffProperty',
                'title': propertyName,
                'type': 'boolean',
                'description': 'Digital input ' + propertyName
            }
        )
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update,
            int(_config.setting('FASTUPDATEINTERVAL')) * 1000
        )
        self.timer.start()

    def update(self):
        value = self.bridge.read_digital(self.inputPin)
        self.inputValue.notify_of_external_update(value)

    def cancel(self):
        self.timer.stop()
################################################################################

################################################################################
class AnalogInput_property(Property):
    """Single analog input."""

    def __init__(self, theThing, propertyName='', enablePin=0, analogPin=0):
        self.enablePin = enablePin
        self.analogPin = analogPin
        self.inputValue = Value(0.0)
        if (theThing.bridge):
            self.bridge = theThing.bridge
        else:
            self.bridge = SensorBridge(SENSORBRIDGEADDRESS)
        self.bridge.write_digital(self.enablePin, False)
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
        self.bridge.write_digital(self.enablePin, True)
        sleep(1)
        value = self.bridge.read_analog(self.analogPin)
        self.bridge.write_digital(self.enablePin, False)
        self.inputValue.notify_of_external_update(value)

    def cancel(self):
        self.timer.stop()
################################################################################
