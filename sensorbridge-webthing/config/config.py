###############################################################################
#
# (c) 2021 Copyright A-Vision Software
#
# File description :        WebThings Property names
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
        #print(self.ini.sections())

    def name(self, parameter):
        return self.ini['names'][parameter]
