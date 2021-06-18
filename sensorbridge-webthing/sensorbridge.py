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
from webthing import (Action, Event, MultipleThings, Property, Thing, Value, WebThingServer)
from properties import sensorbridge
import devices.SensorBridge

from config import config
_config = config.Config('sensorbridge')
SENSORBRIDGEADDRESS = int(_config.setting('i2c.SENSORBRIDGEADDRESS'))
_sensorbridge = devices.SensorBridge.SensorBridge(SENSORBRIDGEADDRESS)


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
        self.bridge = _sensorbridge

        self.add_property(sensorbridge.DigitalOutput_property(self, _config.name('D1'), 0))
        self.add_property(sensorbridge.DigitalOutput_property(self, _config.name('D2'), 1))
        self.add_property(sensorbridge.DigitalOutput_property(self, _config.name('D3'), 2))
        self.add_property(sensorbridge.DigitalOutput_property(self, _config.name('D4'), 4))
        self.add_property(sensorbridge.DigitalOutput_property(self, _config.name('D5'), 5))
        self.add_property(sensorbridge.DigitalOutput_property(self, _config.name('D6'), 6))


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
        self.bridge = _sensorbridge

        self.set_ui_href('https://raspberry.a-vision.solutions/greenhouse/settings.html')
        self.add_property(sensorbridge.AnalogInput_property(self, _config.name('A1I'), 3, 0))
        self.add_property(sensorbridge.AnalogInput_property(self, _config.name('A2I'), 7, 1))

    def update_levels(self):
        for prop in self.properties:
            self.properties[prop].update()

    def cancel_update_level_task(self):
        for prop in self.properties:
            self.properties[prop].cancel()


def run_server():
    sensors = AnalogSensors()
    sensors.update_levels()
    activators = DigitalOutputs()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([sensors, activators], 'SensorBridgeDevice'), port=int(_config.setting('WEBTHINGSERVERPORT')))
    try:
        logging.info('starting the server')
        server.start()
    except:
        logging.debug('canceling the sensors update looping task')
        sensors.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=int(_config.setting('DEBUGLEVEL')),
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
