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

from webthing import (Action, Event, MultipleThings, Property, Thing, Value, WebThingServer)
import logging
import names
import constants
import properties

class DigitalOutputs(Thing):
    """Free definable digital oututs."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:greenhouse-analog-sensors',
            names.SBDIGITAL,
            ['OnOffSwitch'],
            names.SBDIGITAL
        )

        self.add_property(properties.SensorBridgeDigitalOutput_property(self, names.D1, 0))
        self.add_property(properties.SensorBridgeDigitalOutput_property(self, names.D2, 1))
        self.add_property(properties.SensorBridgeDigitalOutput_property(self, names.D3, 2))
        self.add_property(properties.SensorBridgeDigitalOutput_property(self, names.D4, 4))
        self.add_property(properties.SensorBridgeDigitalOutput_property(self, names.D5, 5))
        self.add_property(properties.SensorBridgeDigitalOutput_property(self, names.D6, 6))


class AnalogSensors(Thing):
    """Free definable analog sensors, levels in percent."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:greenhouse-analog-sensors',
            names.SBANALOG,
            ['MultiLevelSensor'],
            names.SBANALOG
        )
        self.set_ui_href('https://raspberry.a-vision.solutions/greenhouse/settings.html')
        self.add_property(properties.SensorBridgeAnalogInput_property(self, names.A1I, 3, 0))
        self.add_property(properties.SensorBridgeAnalogInput_property(self, names.A2I, 7, 1))

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
    server = WebThingServer(MultipleThings([sensors, activators], 'SensorBridgeDevice'), port=8881)
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
        level=constants.DEBUGLEVEL,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
