# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import unittest

from diagnostics import _py3k as py3k
from diagnostics.formatters import HtmlFormatter


class TestHtmlFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = HtmlFormatter()

    def test_escape_html(self):
        returned = self.formatter.escape_html(
            "<script>var v = true && false, s = 'ščťžý'</script>")
        expected = "&lt;script&gt;var v = true &amp;&amp; false, s = 'ščťžý'&lt;/script&gt;"

        self.assertEqual(expected, returned)

    def test_escape_attribute(self):
        returned = self.formatter.escape_attribute(
            "http://...?q='required' <tag>&specialchar=\"")
        expected = "http://...?q=&#039;required&#039; &lt;tag&gt;&amp;specialchar=&quot;"

        self.assertEqual(expected, returned)
