# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import logging as pylogging

from . import logging
from .formatters import HtmlFormatter
from .models import ExceptionInfo
from .storages import FileStorage
from ._py3k import string_types, to_unicode


__author__ = "Michal Belica"
__version__ = "0.2.3"


class _ExceptionHook(object):
    def __init__(self):
        self.storage = None
        self.formatter = None

    def enable(self, storage=None, formatter=HtmlFormatter()):
        if not storage:
            storage = FileStorage()

        self.storage = storage
        self.formatter = formatter

        sys.excepthook = self

    def enable_for_logger(self, logger, handler):
        if isinstance(logger, string_types):
            logger = pylogging.getLogger(logger)

        formatter = logging.HtmlFormatter("%(asctime)s [%(levelname)s]: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def __call__(self, type, value, traceback):
        exception_info = ExceptionInfo.from_values(type, value, traceback)

        try:
            data = self.formatter.format_exception(exception_info)
        except:
            data = "<p><pre>%s\n%s</pre></p>" % (
                to_unicode(exception_info),
                to_unicode(ExceptionInfo.new()),
            )

        self.storage.save(data, exception_info)

    def __enter__(self):
        if not self.storage:
            self.storage = FileStorage()
        if not self.formatter:
            self.formatter = HtmlFormatter()

    def __exit__(self, type, value, traceback):
        if (type, value, traceback) != (None, None, None):
            self(type, value, traceback)

        # suppress exception
        return True


exception_hook = _ExceptionHook()
