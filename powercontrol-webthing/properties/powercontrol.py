###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        PowerControl properties
#
# Created by       :        Arnold Velzel
# Created on       :        24-05-2021
#
################################################################################

import logging
import tornado.ioloop
from webthing import (Property, Value)
from devices.MCP3425 import MCP3425
from devices.TMP75 import TMP75
from .raspberry import PWM_property

from config import config
_config = config.Config('powercontrol')

################################################################################
class PowerOutput_property(PWM_property):
    """PWM output"""

    def __init__(self, theThing, propertyName='', outputPin=0):
        PWM_property.__init__(self, theThing, propertyName, outputPin)
################################################################################

################################################################################
class Temperature_property(Property):
    """Temperature sensor."""

    def __init__(self, theThing, propertyName=''):
        self.tmp75 = TMP75()
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
            int(_config.setting('FASTUPDATEINTERVAL')) * 1000
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
class LoadCurrent_property(Property):
    """Single analog input."""

    def __init__(self, theThing, propertyName=''):
        self.mcp3425 = MCP3425()
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
            int(_config.setting('FASTUPDATEINTERVAL')) * 1000
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