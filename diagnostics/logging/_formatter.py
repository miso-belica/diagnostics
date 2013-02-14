# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from logging import Formatter as LoggingFormatter
from ..formatters import HtmlFormatter as Formatter
from ..models import ExceptionInfo
from .._py3k import to_unicode


class HtmlFormatter(LoggingFormatter):
    def format_exception(self, exception_info, user_message=None):
        try:
            formatter = Formatter()
            return formatter.format_exception(exception_info, user_message)
        except:
            return "<p><pre>%s\n%s</pre></p>" % (
                to_unicode(ExceptionInfo.from_values(exception_info)),
                to_unicode(ExceptionInfo.new()),
            )

    # compatibility with logging module
    formatException = format_exception
