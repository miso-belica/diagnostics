# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import inspect

from os.path import abspath
from .variable import Variable
from .code import CodeLine


class Frame(object):
    def __init__(self, frame, number):
        self._number = number
        self._frame = frame
        self._function_arguments, self._locals = self._build_locals()
        self._globals = self._build_globals()

    @property
    def number(self):
        return self._number

    @property
    def path_to_file(self):
        return abspath(inspect.getframeinfo(self._frame).filename)

    @property
    def source_line(self):
        return inspect.getframeinfo(self._frame).lineno

    @property
    def locals(self):
        return self._locals

    @property
    def globals(self):
        return self._globals

    @property
    def routine_name(self):
        return inspect.getframeinfo(self._frame).function

    @property
    def routine_arguments(self):
        return self._function_arguments

    def lines(self, count=1):
        frame_info = inspect.getframeinfo(self._frame, count)
        return self._build_context_lines(frame_info.code_context,
            frame_info.lineno, frame_info.index)

    def _build_context_lines(self, lines, first_line_number, source_line_index):
        # code is probably in binary form
        if lines is None:
            return (CodeLine(first_line_number,
                "Code not discovered (probably compiled from C/C++ code)",
                exception_source=True),)

        context_lines = []
        for line_index, line in enumerate(lines):
            line_number = first_line_number + line_index
            is_exception_source = bool(line_index == source_line_index)

            context_lines.append(CodeLine(line_number, line, is_exception_source))

        return tuple(context_lines)

    def _build_locals(self):
        params, args, kwargs, local_vars = inspect.getargvalues(self._frame)

        local_variables = []
        function_arguments = []
        for var_name, var_value in sorted(local_vars.items()):
            variable = Variable(var_name, var_value)
            if var_name in params or var_name in (args, kwargs):
                function_arguments.append(variable)
            elif not variable.is_magic():
                local_variables.append(variable)

        return tuple(function_arguments), tuple(local_variables)

    def _build_globals(self):
        return Variable.map(self._frame.f_globals.items())
