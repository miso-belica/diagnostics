# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import datetime

from os.path import dirname, abspath, join, exists
from .._py3k import to_unicode, get_working_directory


def timestamp(format="%Y-%m-%d %H:%M:%S"):
    return to_unicode(datetime.datetime.now().strftime(format))


def path_relative_to_main_module(path):
    try:
        directory = dirname(sys.modules["__main__"].__file__)
    except AttributeError: # executed from terminal
        directory = get_working_directory()

    directory = abspath(directory)
    return to_unicode(join(directory, path))


def read_resource_data(path):
    path = expand_file_resource(path)
    if not exists(path):
        raise ValueError("Resource for given path doesn't exist: " + path)

    with open(path, "rb") as file:
        return file.read().decode("utf8")


def expand_file_resource(path):
    directory = dirname(sys.modules["diagnostics"].__file__)
    directory = abspath(directory)
    return join(directory, path)


def python_version():
    return to_unicode(sys.version)


def path_to_executable():
    return to_unicode(sys.executable)


def working_directory():
    return get_working_directory()


def arguments_vector():
    return list(map(to_unicode, sys.argv))


def command_line_arguments():
    return arguments_vector()[1:]


def program_name():
    return to_unicode(sys.argv[0])
