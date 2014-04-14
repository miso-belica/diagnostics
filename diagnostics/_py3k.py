# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sys import version_info


PY3 = version_info[0] == 3


if PY3:
    bytes = bytes
    unicode = str
else:
    bytes = str
    unicode = unicode
string_types = (bytes, unicode,)


try:
    from types import ClassType
    class_types = (ClassType, type)
except ImportError:
    class_types = type


try:
    from urllib.parse import quote as quote_query
except ImportError:
    from urllib import quote as quote_query


try:
    from os import getcwdu as get_working_directory
except ImportError:
    from os import getcwd as get_working_directory


def to_string(object):
    return to_unicode(object) if PY3 else to_bytes(object)


def to_bytes(object):
    try:
        if isinstance(object, bytes):
            return object
        elif isinstance(object, unicode):
            return object.encode("utf-8")
        else:
            # try encode instance to bytes
            return instance_to_bytes(object)
    except UnicodeError:
        # recover from codec error and use 'repr' function
        return to_bytes(repr(object))


def to_unicode(object):
    try:
        if isinstance(object, unicode):
            return object
        elif isinstance(object, bytes):
            return object.decode("utf-8")
        else:
            # try decode instance to unicode
            return instance_to_unicode(object)
    except UnicodeError:
        # recover from codec error and use 'repr' function
        return to_unicode(repr(object))


def instance_to_bytes(instance):
    if PY3:
        if hasattr(instance, "__bytes__"):
            return bytes(instance)
        elif hasattr(instance, "__str__"):
            return unicode(instance).encode("utf-8")
    else:
        if hasattr(instance, "__str__"):
            return bytes(instance)
        elif hasattr(instance, "__unicode__"):
            return unicode(instance).encode("utf-8")

    return to_bytes(repr(instance))


def instance_to_unicode(instance):
    if PY3:
        if hasattr(instance, "__str__"):
            return unicode(instance)
        elif hasattr(instance, "__bytes__"):
            return bytes(instance).decode("utf-8")
    else:
        if hasattr(instance, "__unicode__"):
            return unicode(instance)
        elif hasattr(instance, "__str__"):
            return bytes(instance).decode("utf-8")

    return to_unicode(repr(instance))
