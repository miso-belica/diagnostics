# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import inspect

from traceback import format_exception
from .._py3k import to_unicode, to_string, callable
from .variable import Variable
from .frame import Frame


class ExceptionInfo(tuple):
    @classmethod
    def from_values(cls, *values):
        if len(values) != 3:
            raise ValueError("Only `sys.exc_info` compatible tuple is supported")

        return cls(values)

    @classmethod
    def new(cls):
        return cls(sys.exc_info())

    @property
    def type_name(self):
        return to_unicode(self.type.__name__)

    @property
    def type(self):
        return self[0]

    @property
    def exception(self):
        return self[1]

    @property
    def exception_description(self):
        return to_unicode(self.exception.__doc__)

    @property
    def traceback(self):
        return self[2]

    @property
    def message(self):
        args = self.exception.args
        # by convention 1st argument of Exception is message
        return to_unicode(args[0] if args else self.exception)

    @property
    def frames(self):
        frames = []

        frame_order = 1
        traceback = self.traceback
        while traceback:
            frames.append(Frame(traceback.tb_frame, frame_order))
            traceback = traceback.tb_next
            frame_order += 1

        return tuple(frames)

    @property
    def exception_attributes(self):
        attributes = inspect.getmembers(self.exception,
            lambda a: not callable(a))

        return Variable.map(attributes)

    def __str__(self):
        lines = format_exception(*self)
        return to_string("").join(to_string(l) for l in lines)