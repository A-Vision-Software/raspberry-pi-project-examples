###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        WebThings properties
#
# Created by       :        Arnold Velzel
# Created on       :        24-05-2021
#
################################################################################

from gpiozero import PWMOutputDevice, DigitalOutputDevice, InputDevice
from webthing import (Property, Value)
from time import sleep
import devices
import logging
import constants
import tornado.ioloop
from i2csensorbridge import SensorBridge

################################################################################
class PWM_property(Property):
    """PWM output"""

    def __init__(self, theThing, propertyName='', outputPin=0):
        self.output = PWMOutputDevice(outputPin, active_high=True, frequency=30)
        self.outputValue = Value(0.0, lambda v: self.setOutput(v))
        Property.__init__(
            self,
            thing=theThing,
            name=propertyName,
            value=self.outputValue,
            metadata={
                '@type': 'LevelProperty',
                'title': propertyName,
                'type': 'number',
                'minimum': 0,
                'maximum': 100,
                'unit': 'percent',
                'description': 'PWM output ' + propertyName
            }
        )

    def setOutput(self, v):
        if (v):
            self.output.value = v / 100
        else:
            self.output.value = 0
################################################################################

################################################################################
class DigitalOutput_property(Property):
    """Single digital output."""

    def __init__(self, theThing, propertyName='', outputPin=0):
        self.outputPin = outputPin
        self.outputValue = Value(0.0, lambda v: self.setOutput(v))
        self.output = DigitalOutputDevice(self.outputPin, active_high=True)
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
            self.output.on()
        else:
            logging.debug('Set pin OFF')
            self.output.off()
################################################################################

################################################################################
class MCP3425_property(Property):
    """Single analog input."""

    def __init__(self, theThing, propertyName=''):
        self.mcp3425 = devices._MCP3425()
        self.available = self.mcp3425.available()
        if not self.available:
            logging.warning('MCP3425 device not found')
            propertyName = 'FAKE: ' + propertyName
            self.available = False

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
                'maximum': 2048,
                'readOnly': True,
                'description': 'Analog input ' + propertyName
            }
        )
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update,
            constants.FASTUPDATEINTERVAL * 1000
        )
        self.timer.start()

    def update(self):
        if self.available:
            value = self.mcp3425.read()
        else :
            value = 0
        self.inputValue.notify_of_external_update(value)

    def cancel(self):
        self.timer.stop()
################################################################################

################################################################################
class TMP75_property(Property):
    """Temperature sensor."""

    def __init__(self, theThing, propertyName=''):
        self.tmp75 = devices._TMP75()
        self.available = self.tmp75.available()
        if not self.available:
            logging.warning('TMP75 device not found')
            propertyName = 'FAKE: ' + propertyName
            self.available = False

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
                'minimum': -40,
                'maximum': 125,
                'unit': '°C',
                'readOnly': True,
                'description': 'Temperature ' + propertyName
            }
        )
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update,
            constants.FASTUPDATEINTERVAL * 1000
        )
        self.timer.start()

    def update(self):
        if self.available:
            value = self.tmp75.read()
        else :
            value = 0
        self.inputValue.notify_of_external_update(value)

    def cancel(self):
        self.timer.stop()
################################################################################

################################################################################
class SHT20_property(Property):
    """Temperature sensor"""

    def __init__(self, theThing, propertyName='', parameter=''):
        self.parameter = parameter
        self.sht = devices._SHT20()
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
            constants.FASTUPDATEINTERVAL * 1000
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

################################################################################
class ADS1015_property(Property):
    """Single analog input."""

    def __init__(self, theThing, propertyName='', enablePin=0, analogPin=0):
        self.adc = devices._ADS1015()
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
            (constants.SLOWUPDATEINTERVAL + analogPin*2) * 1000,
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
class SensorBridgeDigitalOutput_property(Property):
    """Single digital output."""

    def __init__(self, theThing, propertyName='', outputPin=0):
        self.outputPin = outputPin
        self.outputValue = Value(0.0, lambda v: self.setOutput(v))
        self.bridge = SensorBridge(devices.SENSORBRIDGEADDRESS)
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
class SensorBridgeDigitalInput_property(Property):
    """Single digital input."""

    def __init__(self, theThing, propertyName='', inputPin=0):
        self.inputPin = inputPin
        self.inputValue = Value(0.0)
        self.bridge = SensorBridge(devices.SENSORBRIDGEADDRESS)
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
            constants.FASTUPDATEINTERVAL * 1000
        )
        self.timer.start()

    def update(self):
        value = self.bridge.read_digital(self.inputPin)
        self.inputValue.notify_of_external_update(value)

    def cancel(self):
        self.timer.stop()
################################################################################

################################################################################
class SensorBridgeAnalogInput_property(Property):
    """Single analog input."""

    def __init__(self, theThing, propertyName='', enablePin=0, analogPin=0):
        self.enablePin = enablePin
        self.analogPin = analogPin
        self.inputValue = Value(0.0)
        self.bridge = SensorBridge(devices.SENSORBRIDGEADDRESS)
        self.bridge.write_digital(self.enablePin, False)
        Property.__init__(
            self,
            thing=theThing,
            name=propertyName,
            value=self.inputValue,
            metadata={
                '@type': 'OnOffProperty',
                'title': propertyName,
                'type': 'boolean',
                'description': 'Analog input ' + propertyName
            }
        )
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update,
            (constants.SLOWUPDATEINTERVAL + analogPin*2) * 1000,
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

