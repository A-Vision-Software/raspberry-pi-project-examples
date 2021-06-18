###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        WebThings config
#
# Created by       :        Arnold Velzel
# Created on       :        24-05-2021
#
################################################################################

import configparser
import pathlib

class Config():

    def __init__(self, name):
        self.path = pathlib.Path(__file__).parent.absolute()
        self.ini = configparser.ConfigParser()
        self.ini.read(str(self.path) + '/' + name + '.ini')

        self.system = configparser.ConfigParser()
        self.system.read(str(self.path) + '/system.ini')

    def name(self, parameter):
        return self.ini['names'][parameter]

    def setting(self, parameter):
        try:
            section, parametername = parameter.split(".")
        except:
            section = 'system'
            parametername = parameter

        return self.system[section][parametername]
