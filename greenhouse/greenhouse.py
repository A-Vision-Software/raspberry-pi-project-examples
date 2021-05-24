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

from __future__ import division, print_function
from webthing import (Action, Event, MultipleThings, Property, Thing, Value, WebThingServer)
import logging
import properties
import names
import constants

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


        self.add_property(properties.SHT20_property(self,'Temperature','temperature'))
        self.add_property(properties.SHT20_property(self,'Humidity','humidity'))

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
            names.DIGITAL,
            ['OnOffSwitch'],
            names.DIGITAL
        )

        self.add_property(properties.DigitalOutput_property(self, names.DIGITAL1, 18))
        self.add_property(properties.DigitalOutput_property(self, names.DIGITAL2, 19))
        self.add_property(properties.DigitalOutput_property(self, names.DIGITAL3, 20))
        self.add_property(properties.DigitalOutput_property(self, names.DIGITAL4, 21))

class AnalogSensors(Thing):
    """Free definable analog sensors, levels in percent."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:greenhouse-analog-sensors',
            names.ANALOG,
            ['MultiLevelSensor'],
            names.ANALOG
        )

        self.add_property(properties.ADS1015_property(self, names.ANALOG1, 22, 0))
        self.add_property(properties.ADS1015_property(self, names.ANALOG2, 23, 1))
        self.add_property(properties.ADS1015_property(self, names.ANALOG3, 24, 2))
        self.add_property(properties.ADS1015_property(self, names.ANALOG4, 25, 3))

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
    server = WebThingServer(MultipleThings([sensors, humidity_temperature, activators], 'GreenhouseDevice'), port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensors update looping task')
        sensors.cancel_update_level_task()
        humidity_temperature.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=constants.DEBUGLEVEL,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
