#!/usr/bin/python3

################################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        Python power control Thing
#
# Created by       :        Arnold Velzel
# Created on       :        23-05-2021
#
################################################################################

import logging
#from __future__ import division, print_function
from config import config
from webthing import (Action, Event, MultipleThings, Property, Thing, Value, WebThingServer)
from properties.raspberry import DigitalOutput_property
from properties.greenhouse import TemperatureHumidity_property
from properties.greenhouse import AnalogInput_property

_config = config.Config('greenhouse')

class HumidityTempSensor(Thing):
    """A humidity / temperature sensor which updates its measurement every few seconds."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:greenhouse-humidity-temperature-sensor',
            'Greenhouse Temperature and Humidity',
            ['MultiLevelSensor'],
            'Greenhouse Humidity and Temperature'
        )

        self.add_property(TemperatureHumidity_property(self,'Temperature','temperature'))
        self.add_property(TemperatureHumidity_property(self,'Humidity','humidity'))

    def update_levels(self):
        for prop in self.properties:
            self.properties[prop].update()

    def cancel_update_level_task(self):
        for prop in self.properties:
            self.properties[prop].cancel()


class DigitalOutputs(Thing):
    """Free definable digital oututs."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:greenhouse-analog-sensors',
            _config.name('DIGITAL'),
            ['OnOffSwitch'],
            _config.name('DIGITAL')
        )

        self.add_property(DigitalOutput_property(self, _config.name('O18'), 18))
        self.add_property(DigitalOutput_property(self, _config.name('O19'), 19))
        self.add_property(DigitalOutput_property(self, _config.name('O20'), 21))
        self.add_property(DigitalOutput_property(self, _config.name('O21'), 20))


class AnalogSensors(Thing):
    """Free definable analog sensors, levels in percent."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:greenhouse-analog-sensors',
            _config.name('ANALOG'),
            ['MultiLevelSensor'],
            _config.name('ANALOG')
        )
        self.set_ui_href('https://raspberry.a-vision.solutions/greenhouse/settings.html')
        self.add_property(AnalogInput_property(self, _config.name('AI0'), 22, 0))
        self.add_property(AnalogInput_property(self, _config.name('AI1'), 23, 1))
        self.add_property(AnalogInput_property(self, _config.name('AI3'), 24, 2))
        self.add_property(AnalogInput_property(self, _config.name('AI2'), 25, 3))

    def update_levels(self):
        for prop in self.properties:
            self.properties[prop].update()

    def cancel_update_level_task(self):
        for prop in self.properties:
            self.properties[prop].cancel()


def run_server():
    sensors = AnalogSensors()
    sensors.update_levels()

    humidity_temperature = HumidityTempSensor()
    humidity_temperature.update_levels()

    activators = DigitalOutputs()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([sensors, humidity_temperature, activators], 'GreenhouseDevice'), port=8881)
    try:
        logging.info('starting the server')
        server.start()
    except:
        logging.debug('canceling the sensors update looping task')
        sensors.cancel_update_level_task()
        humidity_temperature.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=_config.setting('DEBUGLEVEL'),
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
