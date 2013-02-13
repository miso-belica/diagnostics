# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import os
import sys
import datetime

from os.path import dirname, abspath, join
from .._py3k import to_unicode, get_working_directory


class Environment(object):
    def timestamp(self, format="%Y-%m-%d %H:%M:%S"):
        return to_unicode(datetime.datetime.now().strftime(format))

    def path_relative_to_main_module(self, path):
        directory = dirname(self.main_module.__file__)
        directory = abspath(directory)
        return to_unicode(join(directory, path))

    def expand_file_resource(self, path):
        directory = dirname(sys.modules["diagnostics"].__file__)
        directory = abspath(directory)
        return join(directory, path)

    @property
    def main_module(self):
        return sys.modules["__main__"]

    @property
    def python_version(self):
        return to_unicode(sys.version)

    @property
    def path_to_executable(self):
        return to_unicode(sys.executable)

    @property
    def working_directory(self):
        return get_working_directory()

    @property
    def arguments_vector(self):
        return tuple(map(to_unicode, sys.argv))

    @property
    def command_line_arguments(self):
        return self.arguments_vector[1:]

    @property
    def program_name(self):
        return to_unicode(sys.argv[0])
