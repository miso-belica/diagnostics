# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import unittest

from exc_utils import get_exception_info_1
from diagnostics import _py3k as py3k
from diagnostics.models.excinfo import ExceptionInfo


class TestExceptionInfo(unittest.TestCase):
    def test_compatibility_with_exc_info_result(self):
        info = get_exception_info_1()

        self.assertTrue(isinstance(info, tuple))
        self.assertEqual(len(info), 3)

        exception_type, exception, traceback = info
        self.assertTrue(isinstance(exception_type, type))
        self.assertTrue(isinstance(exception, Exception))

    def test_new_interface(self):
        message = "Something went wrong..."
        info = get_exception_info_1(message)

        self.assertEqual(info.type_name, "Exception")
        self.assertTrue(isinstance(info.type, type))
        self.assertTrue(isinstance(info.exception, Exception))
        self.assertEqual(info.message, message)

    def test_exception_attributes(self):
        ATTRIBUTES = {
            "args": ("1", 2, 3.0,),
            "pepek": "spinach",
        }

        if not py3k.PY3:
            # message attribute was removed in py3k
            # message is set to 1st argument only if it is the only argument
            ATTRIBUTES["message"] = ""

        info = get_exception_info_1("1", 2, 3.0)
        info.exception.pepek = "spinach"

        attribute_names = tuple(a.name for a in info.exception_attributes)
        for attr_name in ATTRIBUTES:
            self.assertTrue(attr_name in attribute_names)

        for a in info.exception_attributes:
            self.assertTrue(a.name in ATTRIBUTES)
            self.assertEqual(ATTRIBUTES[a.name], a.value)

    def test_info_wtihout_exception_raised(self):
        """
        This happes when somebody logs traceback but no exception
        was raised: logger.error("message", exc_info=True)
        """
        info = ExceptionInfo.new()

        self.assertEqual(info.type_name, None)
        self.assertEqual(info.type, None)
        self.assertEqual(info.exception, None)
        self.assertEqual(info.exception_description, "")
        self.assertEqual(info.traceback, None)
        self.assertEqual(info.frames, ())
        self.assertEqual(info.exception_attributes, ())
