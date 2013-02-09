===========
Diagnostics
===========
Module for logging of detail traceback as HTML page. Unexpected exceptions are
catched and logged for further audit. Exceptions in diagnostic's exception
handler are properly handled and logged (but formatted only as standard Python
traceback). Usage is simple as code below

.. code-block:: python

    # you have to create "log/" directory next to file that is your main module
    import diagnostics

    # or simply set your own storage
    from diagnostics.storages import FileStorage
    dignostics.exception_hook.storage = FileStorage(
        "/path/to/your/log/directory/with/html/tracebacks")

Installation
------------
Currently only from git repo
::

    pip install git+git@github.com:miso-belica/diagnostics.git

Tests
-----
Run tests via

.. code-block:: bash

    $ cd tests
    $ python -tt -Wall -B -3 -m unittest discover
    $ python3 -tt -Wall -B -m unittest discover

Copyright 2013 Michal Belica
