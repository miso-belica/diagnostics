# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import os
import sys

from .models import Environment
from . import _py3k as py3k


class FileStorage(object):
    def __init__(self, directory_path=None):
        if not directory_path:
            directory_path = self._determine_directory_path()

        self._directory_path = py3k.to_unicode(directory_path)
        self._check_directory_path(self._directory_path)

    def _determine_directory_path(self):
        env = Environment()
        return env.path_relative_to_main_module("log/")

    def save(self, data, exception_info):
        file_path = self._build_path_to_file(exception_info)
        self._write(data, file_path)

    def _check_directory_path(self, directory_path):
        if not os.path.exists(directory_path):
            raise ValueError("Path '%s' does not exists" % directory_path)

        if not os.path.isdir(directory_path):
            raise ValueError("Path '%s' is not a directory" % directory_path)

        if not os.access(directory_path, os.W_OK):
            raise ValueError("Directory '%s' is not writable" % directory_path)

    def _build_path_to_file(self, exception_info):
        timestamp = Environment().timestamp("%Y-%m-%d %H-%M-%S")
        exception_type = exception_info.type_name

        filename = self._build_filename(exception_type, timestamp)
        path = os.path.join(self._directory_path, filename)

        order = 1
        while os.path.exists(path):
            filename = self._build_filename(exception_type, timestamp, order)
            path = os.path.join(self._directory_path, filename)

        return path

    def _build_filename(self, exception_type, timestamp, suffix=None):
        return "%s %s%s.html" % (
            exception_type,
            timestamp,
            ("_" + py3k.to_unicode(suffix)) if suffix else "",
        )

    def _write(self, data, path_to_file):
        with open(path_to_file, "ab") as file:
            file.write(py3k.to_bytes(data))
