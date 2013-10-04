# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from itertools import dropwhile


def strip(haystack, predicate=bool):
    return rstrip(lstrip(haystack, predicate), predicate)


def lstrip(haystack, predicate=bool):
    return list(dropwhile(predicate, haystack))


def rstrip(haystack, predicate=bool):
    haystack = reversed(tuple(haystack))
    stripped = dropwhile(predicate, haystack)
    return list(reversed(tuple(stripped)))
