===========
Diagnostics
===========
Module for logging of `detailed traceback
<http://miso-belica.github.com/diagnostics/log-example.html>`_ as HTML page.
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

    if __name__ == '__main__':
        exception_hook.enable_for_logger(logging.getLogger())

        try:
            try_do_risky_job(...)
        except:
            logging.exception("Risky job failed")

.. code-block:: python

    import logging

    from diagnostics import exception_hook

    if __name__ == '__main__':
        logger = logging.getLogger("logger")
        directory_path = "/path/to/your/log/directory/with/html/tracebacks"
        exception_hook.enable_for_logger(logger, directory_path)

        try:
            try_do_risky_job(...)
        except:
            logging.error("Error occured", exc_info=True)

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

    $ cd tests
    $ python -tt -Wall -B -3 -m unittest discover
    $ python3 -tt -Wall -B -m unittest discover
