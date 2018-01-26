# -*- coding: utf-8 -*-
# Copyright (c) 2013 Federico Ruiz-Ugalde
# Author: Federico Ruiz Ugalde <memeruiz at gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# You can use this class to get a python file (used as a config file) in any
# directory and get it imported in your program as a variable with method
# get_config or get_all. Also you can add additional cmdline argument options
# using object.parser.add_option as explained in the optparse python
# documentation and then using get_all() method to obtain the parsed output

from __future__ import print_function
import optparse
import sys
import os
from functools import reduce


def import_config(filename):
    config_filename_path = reduce(
        lambda x, y: x + "/" + y,
        filename.split("/")[:-1])
    print("Dir", config_filename_path)
    config_filename_name = filename.split("/")[-1]
    print("ConfigFilename name:", config_filename_name)
    if not os.path.exists(filename):
        print("Config filename: ", config_filename_name, " not found, exiting")
        sys.exit(-1)
    sys.path.append(config_filename_path)
    config = __import__(
        reduce(lambda x, y: x + "." + y,
               config_filename_name.split(".")[:-1]))
    return (config)


class ConfigFileParser(object):
    def __init__(self, argv):
        self.argv = argv
        self.parser = optparse.OptionParser("usage: %prog [options]")
        self.parser.add_option(
            "-c",
            "--configfilename",
            dest="config_filename",
            default="config.py",
            type="string",
            help="config filename")
        # self.parser.add_option(
        #     "-s",
        #     "--simulation",
        #     action="store_true",
        #     dest="sim",
        #     default=False,
        #     help="Simulation")

    def parse(self):
        (self._options, self._args) = self.parser.parse_args(self.argv[1:])
        self._config_filename = self._options.config_filename

    def import_config(self):
        self.parse()
        self._config = import_config(self._config_filename)

    def get_config(self):
        self.import_config()
        return (self._config)

    def get_all(self):
        # Gives you options, args and config as a tuple
        self.import_config()
        return (self._options, self._args, self._config)


# def config_parse(argv):
#     import os
#     sim=False
#     parser.add_option("-s", "--simulation", action="store_true", dest="sim",
#                                             default=False,help="Simulation")
#     (options, args)= parser.parse_args(argv[1:])

#     sim=options.sim

#     config.sim = sim
#     return (config, args)
