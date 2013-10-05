# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import unittest

from diagnostics.models import environment as env


class TestEnvironment(unittest.TestCase):
    def test_resources_correctly_loaded(self):
        data = env.read_resource_data("templates/style.css")
        self.assertTrue(data)

        data = env.read_resource_data("templates/script.js")
        self.assertTrue(data)

    def test_missing_resourcess(self):
        self.assertRaises(ValueError, env.read_resource_data, "missing/file")
