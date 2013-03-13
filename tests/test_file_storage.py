# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import os
import exc_utils
import unittest

from glob import glob
from os.path import abspath, join, dirname, exists as file_exists
from diagnostics import _py3k as py3k
from diagnostics.storages import FileStorage


LOG_DIRECTORY = abspath(join(
    dirname(__file__),
    "data/log"
))


class TestFileStorage(unittest.TestCase):
    def tearDown(self):
        for path in glob(join(LOG_DIRECTORY, "*")):
            os.unlink(path)

    def _get_file_contents(self, path):
        with open(path) as file:
            return file.read()

    def test_log_directory_ok(self):
        FileStorage(LOG_DIRECTORY)

    def test_log_directory_not_exists(self):
        self.assertRaises(ValueError, FileStorage, "blah_directory")

    def test_log_directory_is_not_directory(self):
        self.assertRaises(ValueError, FileStorage, "test_file_storage.py")

    def test_save(self):
        exception_info = exc_utils.get_exception_info_1()

        storage = FileStorage(LOG_DIRECTORY)
        storage.save("test_save", exception_info)

        path = join(LOG_DIRECTORY, exc_utils.EXCEPTION_FILE_NAME_1)
        self.assertTrue(file_exists(path))

    def test_dont_save_duplicate(self):
        path = join(LOG_DIRECTORY, exc_utils.EXCEPTION_FILE_NAME_1)
        exception_info = exc_utils.get_exception_info_1()

        storage = FileStorage(LOG_DIRECTORY)
        storage.save("duplicate:first", exception_info)
        self.assertTrue(file_exists(path))

        # duplicated exception
        exception_info = exc_utils.get_exception_info_1("arg", 25.3, self)
        storage = FileStorage(LOG_DIRECTORY)
        storage.save("duplicate:second", exception_info)

        self.assertEqual("duplicate:first", self._get_file_contents(path))

    def test_save_different_tracebacks(self):
        path_1 = join(LOG_DIRECTORY, exc_utils.EXCEPTION_FILE_NAME_1)
        path_2 = join(LOG_DIRECTORY, exc_utils.EXCEPTION_FILE_NAME_2)

        exception_info = exc_utils.get_exception_info_1()
        storage = FileStorage(LOG_DIRECTORY)
        storage.save("diff:first", exception_info)
        self.assertTrue(file_exists(path_1))

        exception_info = exc_utils.get_exception_info_2()
        storage = FileStorage(LOG_DIRECTORY)
        storage.save("diff:second", exception_info)
        self.assertTrue(file_exists(path_2))

        self.assertEqual("diff:first", self._get_file_contents(path_1))
        self.assertEqual("diff:second", self._get_file_contents(path_2))
