# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from logging import FileHandler as LoggingHandler
from os.path import join
from ..storages import FileStorage
from ..models import ExceptionInfo


class FileHandler(LoggingHandler):
    def __init__(self, directory_path=None):
        self._storage = FileStorage(directory_path)
        path = join(self._storage._directory_path, "info.log")
        super(FileHandler, self).__init__(path, encoding="utf8", delay=True)

    def emit(self, record):
        exception_info = record.exc_info
        record.exc_info = False

        if isinstance(exception_info, tuple):
            exception_info = ExceptionInfo.from_values(*exception_info)
        elif exception_info:
            exception_info = ExceptionInfo.new()

        super(FileHandler, self).emit(record)

        if exception_info:
            data = self.formatter.format_exception(exception_info,
                record.getMessage())
            self._storage.save(data, exception_info)
