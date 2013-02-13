# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from .._py3k import to_unicode, to_string


class CodeLine(object):
    def __init__(self, number, line, exception_source=False):
        self.__line = to_unicode(line.rstrip())
        self.__number = number
        self._exception_source = exception_source

    @property
    def is_exception_source(self):
        return self._exception_source

    @property
    def number(self):
        return self.__number

    def __unicode__(self):
        return self.__line

    def __str__(self):
        return to_string(self.__line)

    def __repr__(self):
        return "<CodeLine#%d [%s]>" % (self.__number, self.__line.encode("utf8"))
