# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re

from .._py3k import to_unicode, to_string, quote_query
from ..models import ExceptionInfo
from ..models import environment


_TEMPLATE_SKELETON = (
    '<!DOCTYPE html>'
    '<html lang="en">'
    '<head>'
        '<meta charset="UTF-8"/>'
        '<meta name="robots" content="noindex,noarchive"/>'
        '<meta name="generator" content="Python diagnostics module"/>'
        '<title>%(html_user_message)s</title>'
        '<style rel="stylesheet" media="screen,projection">%(css_data)s</style>'
    '</head>'
    '<body>'
        '<header>'
            '<h1 title="%(attr_exception_description)s"><a href="#exception-attributes">%(exception_type)s</a></h1>'
            '<p>'
                '%(exception_message)s\n'
                '<a target="_blank" href="http://www.google.com/search?sourceid=python-diagnostics&amp;ie=utf-8&amp;oe=utf-8&amp;q=%(search_query)s">search by Google</a>'
            '</p>'
            '<dl id="exception-attributes" class="folded">%(html_exception_attributes)s</dl>'
        '</header>'

        '<div class="panel">'
            '<h2>Traceback</h2>'
            '<ol>%(frames)s</ol>'
        '</div>'

        '<div class="panel">'
            '<h2>Environment</h2>'
            '<dl>'
                '<dt>Time of report generation</dt><dd>%(timestamp)s</dd>'
                '<dt>Python version</dt><dd>%(python_version)s</dd>'
                '<dt>Path to executable</dt><dd>%(path_to_executable)s</dd>'
                '<dt>Working directory</dt><dd>%(working_directory)s</dd>'
                '<dt>Arguments vector</dt><dd>%(command_line_arguments)s</dd>'
            '</dl>'
        '</div>'

        '<script>%(js_data)s</script>'
        '<!-- <![CDATA[\n'
        '%(original_traceback)s'
        ']]> -->'
    '</body>'
    '</html>'
)
_FRAME_SKELETON = (
    '<li>'
        '<p>'
            '<a href="editor:%(attr_editor_command)s" title="%(attr_full_file_path)s">'
                '%(full_file_path)s'
            '</a> in %(html_full_routine_name_with_module_prefix)s\n'
            '(<a href="#arguments-%(frame_number)s">arguments <abbr>▶</abbr></a>)'
        '</p>'
        '<dl id="arguments-%(frame_number)s" class="folded">%(html_function_arguments)s</dl>'

        '<div id="frame-details-%(frame_number)s" class="folded">'
            '<pre><code><ol start="%(attr_start_line_number)s">%(html_context_lines)s</ol></code></pre>'

            '<div class="frame-variables">'
                '<h3><a href="#locals-%(frame_number)s">Locals <abbr>▶</abbr></a></h3>'
                '<dl id="locals-%(frame_number)s" class="folded">%(html_locals)s</dl>'

                '<h3><a href="#globals-%(frame_number)s">Globals <abbr>▶</abbr></a></h3>'
                '<dl id="globals-%(frame_number)s" class="folded">%(html_globals)s</dl>'
            '</div>'
        '</div>'
    '</li>'
)


class HtmlFormatter(object):
    ENTITIES = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
    }

    def escape_html(self, value):
        value = to_unicode(value)
        return re.sub(r"[<&>]", self.__get_entity, value)

    def escape_attribute(self, value):
        value = to_unicode(value)
        return re.sub(r"[<&>'\"]", self.__get_entity, value)

    def __get_entity(self, match):
        return HtmlFormatter.ENTITIES[match.group()]

    def format_exception(self, exception_info, user_message=None):
        if not isinstance(exception_info, ExceptionInfo):
            exception_info = ExceptionInfo(*exception_info)

        if not user_message:
            user_message = exception_info.message

        return _TEMPLATE_SKELETON % {
            "html_user_message": self.escape_html(user_message),
            "attr_exception_description": self.escape_attribute(
                exception_info.exception_description),
            "html_exception_attributes": self._render_exception_attributes(
                exception_info.exception_attributes),
            "js_data": environment.read_resource_data(
                "templates/script.js"),
            "css_data": environment.read_resource_data(
                "templates/style.css"),
            "exception_type": self.escape_html(exception_info.type_name),
            "exception_message": self.escape_html(exception_info.message),
            "search_query": self._get_search_query(exception_info),
            "timestamp": self.escape_html(environment.timestamp()),
            "python_version": self.escape_html(
                environment.python_version()),
            "path_to_executable": self.escape_html(
                environment.path_to_executable()),
            "working_directory": self.escape_html(
                environment.working_directory()),
            "command_line_arguments": self._render_command_line_arguments(
                environment.arguments_vector()),
            "original_traceback": to_unicode(exception_info),
            "frames": self._render_frames(exception_info.frames),
        }

    def _get_search_query(self, info):
        message = info.message
        for s in ("'", '"', "+", "-", "&", "|",):
            message = message.replace(s, " ")

        query = '"python" %s %s' % (info.type_name, message,)
        # Python 2.6 needs native strings as parameters
        query = quote_query(to_string(query), to_string(""))
        return self.escape_attribute(to_unicode(query))

    def _render_exception_attributes(self, attributes):
        return "".join('<dt>%s : %s</dt><dd>%s</dd>' % (
            self.escape_html(a.name), self.escape_html(a.type_name), self.escape_html(a.value)) for a in attributes)

    def _render_command_line_arguments(self, arguments):
        list_items = "".join('<li>%s</li>' % self.escape_html(a) for a in arguments)
        return '<ol start="0">%s</ol>' % list_items

    def _render_frames(self, frames):
        rendered = []
        for frame in frames:
            rendered.append(self._render_frame(frame))

        return "".join(rendered)

    def _render_frame(self, frame):
        context_lines, source_line_number = frame.lines(10)
        return _FRAME_SKELETON % {
            "frame_number": self.escape_html(frame.number),
            "attr_editor_command": self.escape_attribute(frame.path_to_file),
            "full_file_path": self.escape_html(frame.path_to_file),
            "attr_full_file_path": self.escape_attribute(frame.path_to_file),
            "html_full_routine_name_with_module_prefix": self.escape_html(frame.routine_name),
            "attr_start_line_number": self.escape_attribute(source_line_number),
            "html_function_arguments": self._render_variables(frame.routine_arguments),
            "html_locals": self._render_variables(frame.locals),
            "html_globals": self._render_variables(frame.globals),
            "html_context_lines": self._render_context_lines(context_lines, frame.number),
        }

    def _render_variables(self, variables):
        rendered = []
        for var in variables:
            try:
                variable_value = self.escape_html(var.value)
            except Exception as e:
                variable_value = "Value of variable is unknown because %r was raised" % e

            rendered.append('<dt>%s : %s</dt><dd>%s</dd>' % (
                self.escape_html(var.name),
                self.escape_html(var.type_name),
                # replace empty value by non-breaking space
                "&nbsp;" if variable_value == '' else variable_value
            ))

        return "".join(rendered)

    def _render_context_lines(self, context_lines, frame_number):
        lines = []
        for line in context_lines:
            if line.is_exception_source:
                lines.append('<li data-target-panel="frame-details-%d" class="clickable"><span>%s</span></li>' % (frame_number, self.escape_html(line)))
            else:
                lines.append('<li><span>%s</span></li>' % self.escape_html(line))

        return "".join(lines)
