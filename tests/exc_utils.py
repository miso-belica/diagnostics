# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from diagnostics.models import ExceptionInfo


def get_exception_info_1(*args):
    try:
        raise Exception(*args)
    except:
        return ExceptionInfo.new()


def get_exception_info_2(*args):
    try:
        raise Exception(*args)
    except:
        return ExceptionInfo.new()


def get_exception_info_with_locals(*args):
    local_1 = args[0]

    try:
        raise Exception(*args)
        local_undefined = args[2]
    except:
        local_except = args[1]
        return ExceptionInfo.new()


def get_exception_info_with_2_frames(c_var=None, z_var=None, a_var=None, *extras, **named):
    try:
        _nested_function(c_var, z_var, a_var, **named)
    except:
        return ExceptionInfo.new()


def _nested_function(b_var, c_var, a_var, **named):
    raise Exception(b_var, c_var, a_var)


EXCEPTION_FILE_NAME_1 = "Exception.%s.html" % get_exception_info_1().hash()
EXCEPTION_FILE_NAME_2 = "Exception.%s.html" % get_exception_info_2().hash()
