# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import inspect

from os.path import abspath
from .code import CodeLine
from .variable import Variable
from ..utils import strip
from .._py3k import to_string, to_unicode


class Frame(object):
    def __init__(self, traceback, number):
        self._number = number
        self._traceback = traceback
        self._frame = traceback.tb_frame
        self._globals = self._build_globals()
        self._routine_arguments, self._locals = self._build_locals([v.name for v in self.globals])

    @property
    def number(self):
        return self._number

    @property
    def path_to_file(self):
        return to_unicode(abspath(self._frame.f_code.co_filename))

    @property
    def source_line(self):
        """
        Line number in frame is wrong when exception is raised in context manager.
        But line number in traceback object is correctly set.
        """
        return self._traceback.tb_lineno

    @property
    def locals(self):
        return self._locals

    @property
    def globals(self):
        return self._globals

    @property
    def routine_name(self):
        """Returns name of scope in which was exception raised."""
        return to_unicode(self._frame.f_code.co_name)

    @property
    def routine_arguments(self):
        return self._routine_arguments

    def lines(self, count=1):
        frame_info = inspect.getframeinfo(self._traceback, count)
        return self._build_context_lines(frame_info.code_context,
            frame_info.lineno, frame_info.index)

    def _build_context_lines(self, lines, source_line_number, source_line_index):
        # code is probably in binary form
        if lines is None:
            return (CodeLine(source_line_number,
                "Code not discovered (probably compiled from C/C++ code)",
                exception_source=True),)

        context_lines = []
        for line_index, line in enumerate(lines):
            line_number = source_line_number + (line_index - source_line_index)
            is_exception_source = bool(line_index == source_line_index)

            context_lines.append(CodeLine(line_number, line, is_exception_source))

        return strip(context_lines, lambda l: to_unicode(l) == "")

    def _build_locals(self, globals_names):
        params, args, kwargs, local_vars = inspect.getargvalues(self._frame)

        routine_arguments = self._build_routine_arguments(params, args, kwargs, local_vars)

        param_names = params + [args, kwargs]
        local_variables = self._build_local_variables(local_vars.items(),
            globals_names, param_names)

        return routine_arguments, local_variables

    def _build_routine_arguments(self, params, args, kwargs, local_vars):
        routine_arguments = []

        for name in params:
            value = local_vars.get(name, Variable.UNDEFINED_VALUE)
            variable = Variable(name, value)
            routine_arguments.append(variable)

        if args is not None:
            value = local_vars.get(args, Variable.UNDEFINED_VALUE)
            variable = Variable("*" + args, value)
            routine_arguments.append(variable)

        if kwargs is not None:
            value = local_vars.get(kwargs, Variable.UNDEFINED_VALUE)
            variable = Variable("**" + kwargs, value)
            routine_arguments.append(variable)

        return routine_arguments

    def _build_local_variables(self, local_vars, globals_names, routine_argument_names):
        local_variables = []

        for var_name, var_value in local_vars:
            # skip routine arguments
            if var_name in routine_argument_names or var_name in globals_names:
                continue

            variable = Variable(var_name, var_value)
            if self._is_usefull_variable(variable) and not variable.is_magic():
                local_variables.append(variable)

        return sorted(local_variables, key=lambda v: v.name.lower())

    def _build_globals(self):
        """Returns global variables except classes, builtin types, ..."""
        variables = Variable.map(self._frame.f_globals.items())
        variables = filter(self._is_usefull_variable, variables)

        return tuple(sorted(variables, key=lambda v: v.name.lower()))

    def _is_usefull_variable(self, var):
        return not (var.is_type() or var.is_module() or var.is_function())

    def __repr__(self):
        return to_string("<Frame#%d: %s>") % (
            self.number,
            to_string(self.routine_name),
        )

    __str__ = __repr__
