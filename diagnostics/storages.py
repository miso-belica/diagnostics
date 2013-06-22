# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import os
import glob

from .models import environment
from . import _py3k as py3k


class FileStorage(object):
    def __init__(self, directory_path=None):
        if not directory_path:
            directory_path = self._determine_directory_path()

        self._directory_path = py3k.to_unicode(directory_path)
        self._check_directory_path(self._directory_path)

    def _determine_directory_path(self):
        return environment.path_relative_to_main_module("log/")

    def save(self, data, exception_info):
        file_path = self._build_path_to_file(exception_info)

        if not self._file_exists(file_path):
            self._write(data, file_path)

    def _check_directory_path(self, directory_path):
        if not os.path.exists(directory_path):
            raise ValueError("Path '%s' does not exists" % directory_path)

        if not os.path.isdir(directory_path):
            raise ValueError("Path '%s' is not a directory" % directory_path)

        if not os.access(directory_path, os.W_OK):
            raise ValueError("Directory '%s' is not writable" % directory_path)

    def _build_path_to_file(self, exception_info):
        exception_type = exception_info.type_name
        exception_hash = exception_info.hash()

        filename = self._build_filename(exception_type, exception_hash)
        return os.path.join(self._directory_path, filename)

    def _build_filename(self, exception_type, hash):
        return "%s.%s.html" % (
            exception_type,
            hash,
        )

    def _file_exists(self, path):
        """Like ``os.path.exists`` but expands wildcards."""
        return bool(glob.glob(path))

    def _write(self, data, path_to_file):
        with open(path_to_file, "ab") as file:
            file.write(py3k.to_bytes(data))
