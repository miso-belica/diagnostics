# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from case import unittest
from diagnostics import _py3k as py3k
from diagnostics.models import ExceptionInfo


class TestExceptionInfo(unittest.TestCase):
    def _get_exception_info(self, *args):
        try:
            raise Exception(*args)
        except:
            return ExceptionInfo.new()

    def test_compatibility_with_exc_info_result(self):
        info = self._get_exception_info()

        self.assertIsInstance(info, tuple)
        self.assertEqual(len(info), 3)

        exception_type, exception, traceback = info
        self.assertIsInstance(exception_type, type)
        self.assertIsInstance(exception, Exception)

    def test_new_interface(self):
        message = "Something went wrong..."
        info = self._get_exception_info(message)

        self.assertEqual(info.type_name, "Exception")
        self.assertIsInstance(info.type, type)
        self.assertIsInstance(info.exception, Exception)
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

        info = self._get_exception_info("1", 2, 3.0)
        info.exception.pepek = "spinach"

        attribute_names = tuple(a.name for a in info.exception_attributes)
        for attr_name in ATTRIBUTES:
            self.assertIn(attr_name, attribute_names)

        for a in info.exception_attributes:
            self.assertIn(a.name, ATTRIBUTES)
            self.assertEqual(ATTRIBUTES[a.name], a.value)
