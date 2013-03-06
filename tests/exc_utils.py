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


EXCEPTION_FILE_NAME_1 = "Exception.%s.html" % get_exception_info_1().hash()
EXCEPTION_FILE_NAME_2 = "Exception.%s.html" % get_exception_info_2().hash()
