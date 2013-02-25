.. :changelog:

Changelog for diagnostics module
================================
- *BUG FIX:* Recover when converting object to unicode raises
  exception (e.g. BeautifulSoup).
- *BUG FIX:* Format code context even if code is in binary form
  (e.g. lxml).
- *BUG FIX:* Use `repr` function when instance can't be de/en-coded
  to the unicode/bytes.
- *BUG FIX:* Tracebacks with the same type of exception and timestamp
  are stored to different files.
- *FEATURE* Added support for with statement.
- *FEATURE* Added logging support.

0.1.0 (2013-02-13)
------------------
- First public release.
