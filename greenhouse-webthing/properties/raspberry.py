###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        Generic Raspberry Pi properties
#
# Created by       :        Arnold Velzel
# Created on       :        24-05-2021
#
################################################################################

import logging
from gpiozero import PWMOutputDevice, DigitalOutputDevice, InputDevice
from webthing import (Property, Value)

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
