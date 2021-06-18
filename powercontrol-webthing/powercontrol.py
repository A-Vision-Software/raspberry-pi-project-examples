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
from config import config
from webthing import (Action, Event, MultipleThings, Property, Thing, Value, WebThingServer)
import properties

_config = config.Config('powercontrol')

class PowerOutputThing(Thing):
    """Output power control"""

    def __init__(self, PWMpowerPin=13):
        Thing.__init__(
            self,
            'urn:dev:ops:a-vision-analog-activator',
            _config.name('PWMPOWER'),
            ['MultiLevelSensor'],
            _config.name('PWMPOWER')
        )
        self.add_property(properties.PWM_property(self, _config.name('PWMPOWER'), PWMpowerPin))

class CurrentSensorThing(Thing):
    """Analog current measurement"""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:a-vision-analog-sensors',
            _config.name('MCP3425'),
            ['MultiLevelSensor'],
            _config.name('MCP3425')
        )
        self.add_property(properties.MCP3425_property(self, _config.name('MCP3425')))

    def update_levels(self):
        for prop in self.properties:
            self.properties[prop].update()

    def cancel_update_level_task(self):
        for prop in self.properties:
            self.properties[prop].cancel()


class TemperatureSensorThing(Thing):
    """Temperature measurement"""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:a-vision-temperature-sensors',
            _config.name('TMP75'),
            ['MultiLevelSensor'],
            _config.name('TMP75')
        )

        self.add_property(properties.TMP75_property(self, _config.name('TMP75')))

    def update_levels(self):
        for prop in self.properties:
            self.properties[prop].update()

    def cancel_update_level_task(self):
        for prop in self.properties:
            self.properties[prop].cancel()


def run_server():
    currentSensor = CurrentSensorThing()
    currentSensor.update_levels()
    temperatureSensor = TemperatureSensorThing()
    temperatureSensor.update_levels()
    PWMpower = PowerOutputThing()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([currentSensor, temperatureSensor, PWMpower], 'PowerControlDevice'), port=int(_config.parameter('server.PORT')))
    try:
        logging.info('starting the server')
        server.start()
    except:
        logging.debug('canceling the sensors update looping task')
        currentSensor.cancel_update_level_task()
        temperatureSensor.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=int(_config.setting('DEBUGLEVEL')),
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
