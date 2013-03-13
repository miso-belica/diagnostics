# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


import unittest

from exc_utils import (get_exception_info_1, get_exception_info_with_2_frames,
    get_exception_info_with_locals)
from diagnostics._py3k import unicode


class TestFrame(unittest.TestCase):
    def test_text_properties_are_unicode(self):
        info = get_exception_info_1(3, 2, 1, "pepek")
        for frame in info.frames:
            self.assertTrue(isinstance(frame.path_to_file, unicode))
            self.assertTrue(isinstance(frame.routine_name, unicode))

    def test_routine_arguments_in_right_order(self):
        """
        Arguments shouldn't be sorted or in arbitrary order.
        Order should be the sama as in function signature.
        """
        info = get_exception_info_with_2_frames(3, 2, 1, 0, "pepek", 29.36, unicode)

        frame_1 = info.frames[0]
        arguments = tuple(a.name for a in frame_1.routine_arguments)
        expected = ("c_var", "z_var", "a_var", "*extras", "**named")
        self.assertEqual(arguments, expected)

        frame_2 = info.frames[1]
        arguments = tuple(a.name for a in frame_2.routine_arguments)
        expected = ("b_var", "c_var", "a_var", "**named")
        self.assertEqual(arguments, expected)

    def test_frame_properties(self):
        info = get_exception_info_with_locals(1, 2, 3)

        frame = info.frames[0]
        self.assertTrue(isinstance(frame.number, int))
        self.assertEqual(frame.number, 1)
        self.assertEqual(repr(frame), "<Frame#1: get_exception_info_with_locals>")

    def test_frame_locals(self):
        info = get_exception_info_with_locals(22.22, 33.5)

        frame = info.frames[0]
        self.assertEqual(len(frame.locals), 2)

        self.assertEqual(frame.locals[0].name, "local_1")
        self.assertEqual(frame.locals[0].value, 22.22)

        self.assertEqual(frame.locals[1].name, "local_except")
        self.assertEqual(frame.locals[1].value, 33.5)

    def test_frame_globals(self):
        info = get_exception_info_with_locals(22.22, 33.5)

        frame = info.frames[0]
        self.assertEqual(len(frame.globals), 6)

        self.assertEqual(frame.globals[0].name, "absolute_import")
        self.assertEqual(frame.globals[1].name, "division")
        self.assertEqual(frame.globals[2].name, "EXCEPTION_FILE_NAME_1")
        self.assertEqual(frame.globals[3].name, "EXCEPTION_FILE_NAME_2")
        self.assertEqual(frame.globals[4].name, "print_function")
        self.assertEqual(frame.globals[5].name, "unicode_literals")
