alinkcheck
==========

A link checker that checks the urls in text files - using Python 3.4 and asyncio

Features
~~~~~~~~

Alinkcheck parses text files, and then checks all the urls it finds.
It can be used, for example, to check the links in files output by databases.

The links are checked asynchronously, so the program does not block while waiting for responses.
However, the number of times each domain is checked is limited.
This means that alinkcheck will run slower if the links you are checking are from
a small number of domains.

Use
~~~

alinkcheck [--help] [-vv] [-p] file

The following example shows the basic use of alinkcheck.

::

    alinkcheck list_of_links.txt

The file that alinkcheck checks can be any format (json, xml, etc.) as
long as it is a text file.
Multiple files can be analyzed with one command. For example, the
following command will check the links in two files:

::

    alinkcheck list_of_links.json another_list.txt

A list of the links that could not be connected to are printed out after all the links have been checked.
Adding the '-v' option will show you the links that were redirected,
and adding the '-vv' option will also print out the links that are OK.

The '-p' option will just parse the file(s), print out a list of the links
and then exit.

Dependencies
~~~~~~~~~~~~

Python 3.4, click and aiohttp.

Author
~~~~~~

This program has been developed by David Whitlock.

License
~~~~~~~

Alinkcheck is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.
