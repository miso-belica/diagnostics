===========
Diagnostics
===========
.. image:: https://api.travis-ci.org/miso-belica/diagnostics.png?branch=master
   :target: https://travis-ci.org/miso-belica/diagnostics

Module for logging of `detailed traceback
<http://miso-belica.github.io/diagnostics/log-example.html>`_ as HTML page.
Unexpected exceptions are catched and logged for further audit. Exceptions
in diagnostic's exception handler are properly handled and logged
(but formatted only as standard Python traceback). Usage is simple as code below.

.. code-block:: python

    from diagnostics import exception_hook

    if __name__ == '__main__':
        # you have to create "log/" directory next to file that is your main module
        exception_hook.enable()

.. code-block:: python

    from diagnostics import exception_hook
    from diagnostics.storages import FileStorage

    if __name__ == '__main__':
        # or simply set your own storage
        directory_path = "/path/to/your/log/directory/with/html/tracebacks"
        exception_hook.enable(storage=FileStorage(directory_path))

.. code-block:: python

    from diagnostics import exception_hook

    if __name__ == '__main__':
        with exception_hook:
            try_do_risky_job(...)

There is even support for logging in diagnostics. Class
``diagnostics.logging.FileHandler`` creates files with detailed traceback
and log messages are appended to the file *info.log* in directory with
logged tracebacks.

.. code-block:: python

    import logging

    from diagnostics import exception_hook
    from diagnostics.logging import FileHandler

    if __name__ == '__main__':
        file_path = "/path/to/log/directory/with/html/tracebacks/info.log"
        log_handler = FileHandler(file_path)
        exception_hook.enable_for_logger(logging.getLogger(), handler=log_handler)

        try:
            try_do_risky_job(...)
        except:
            logging.exception("Risky job failed")

.. code-block:: python

    import logging

    from diagnostics import exception_hook
    from diagnostics.logging import FileHandler

    if __name__ == '__main__':
        file_path = "/path/to/log/directory/with/html/tracebacks/info.log"
        log_handler = FileHandler(file_path)
        exception_hook.enable_for_logger("example_logger", handler=log_handler)

        try:
            try_do_risky_job(...)
        except:
            logger = logging.getLogger("example_logger")
            logger.error("Error occured", exc_info=True)

Installation
------------
From PyPI
::

    pip install diagnostics

or from git repo
::

    pip install git+git://github.com/miso-belica/diagnostics.git

Tests
-----
Run tests via

.. code-block:: bash

    $ nosetests-2.6 && nosetests-3.2 && nosetests-2.7 && nosetests-3.3
