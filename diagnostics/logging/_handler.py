# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from os.path import dirname
from logging import FileHandler as LoggingFileHandler
from ..storages import FileStorage
from ..models import ExceptionInfo


class FileHandler(LoggingFileHandler):
    def __init__(self, file_path, mode="a", encoding="utf8", delay=True):
        directory_path = dirname(file_path)
        self._storage = FileStorage(directory_path)
        # super() raises exception in Python 2.6
        # TypeError: super() argument 1 must be type, not classobj
        LoggingFileHandler.__init__(self, file_path, mode, encoding, delay)

    def emit(self, record):
        exception_info = record.exc_info
        record.exc_info = False

        if isinstance(exception_info, tuple):
            exception_info = ExceptionInfo.from_values(*exception_info)
        elif exception_info:
            exception_info = ExceptionInfo.new()

        # super() raises exception in Python 2.6
        # TypeError: super() argument 1 must be type, not classobj
        LoggingFileHandler.emit(self, record)

        if exception_info:
            data = self.formatter.format_exception(exception_info,
                record.getMessage())
            self._storage.save(data, exception_info)
