Aiourlstatus
============

A link checker that checks the urls in text files - using Python 3.5 and asyncio.

Features
~~~~~~~~

Aiourlstatus can be used as a command line application, or it can be imported and
called from an interactive python, or ipython, shell.

Aiourlstatus parses text files, and then checks all the urls it finds.
It can be used, for example, to check the links in files output by databases.

The links are checked asynchronously, so the program does not block while waiting for responses.
However, the number of times each domain is checked is limited.
This means that aiourlstatus will run slower if the links you are checking are from
a small number of domains.

Use
~~~

Please read the `wiki <https://github.com/riverrun/aiourlstatus/wiki>`_ for
information about how to use aiourlstatus.

Dependencies
~~~~~~~~~~~~

Python 3.5, click and aiohttp.

Author
~~~~~~

This program has been developed by David Whitlock.

License
~~~~~~~

Aiourlstatus is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.
