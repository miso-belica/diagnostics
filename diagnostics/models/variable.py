# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import inspect

from .._py3k import to_unicode, to_string, class_types


class Variable(object):
    def __init__(self, name, value):
        self._name = to_unicode(name)
        self._value = value

    @classmethod
    def map(cls, collection):
        """
        Creates collection of variables from iterable object
        of (name, value) pairs. Removes variables with
        name pattern equals to "__name__" (so called magic).
        """
        variables = (cls(n, v) for n, v in collection)
        return tuple(v for v in variables if not v.is_magic())

    @property
    def type_name(self):
        return to_unicode(type(self._value).__name__)

    @property
    def type(self):
        return type(self._value)

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def is_magic(self):
        return self._name.startswith("__") and self._name.endswith("__")

    def is_type(self):
        return isinstance(self._value, class_types)

    def is_module(self):
        return inspect.ismodule(self._value)

    def is_function(self):
        return inspect.isfunction(self._value)

    def __repr__(self):
        return to_string("<Variable %s = %s>") % (
            to_string(self.name),
            to_string(self.value),
        )

    __str__ = __repr__
