.. :changelog:

Changelog for diagnostics module
================================

0.2.0 (2013-06-22)
------------------
- *BUG FIX:* Removed class types, modules and other crap from
  list of global variables.
- *BUG FIX:* Function/method variables are ordered according
  to function/method signature.
- *FEATURE:* The same exceptions are stored only once
  (according to their hash).
- *BUG FIX:* Recover when converting object to unicode raises
  exception (e.g. BeautifulSoup).
- *BUG FIX:* Format code context even if code is in binary form
  (e.g. lxml).
- *BUG FIX:* Use `repr` function when instance can't be de/en-coded
  to the unicode/bytes.
- *BUG FIX:* Tracebacks with the same type of exception and timestamp
  are stored to different files.
- *FEATURE:* Added support for with statement.
- *FEATURE:* Added logging support.

0.1.0 (2013-02-13)
------------------
- First public release.
