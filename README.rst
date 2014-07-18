alinkcheck
==========

A link checker that checks the links in json or text files - using Python 3.4 and asyncio

Features
~~~~~~~~

Alinkcheck parses json or text files, and then checks all the links it finds.

The links are checked asynchronously, which makes the whole process faster.

Use
~~~

alinkcheck [--help] [-vv] [-p] [-k keyname] file

-  multiple files (json or text files) can be analyzed with one command

For example, the following command will check the links in two files:

::

    alinkcheck list_of_links.json another_list.json

A list of the links that could not be connected to are printed out after all the links have been checked.
Adding the '-v' option will show you the links that were redirected,
and adding the '-vv' option will also print out the links that are OK.

The '-p' option will just parse the file(s), print out a list of the links
and then exit.

If you know the name of the key for each url, you can specify the key with the '-k' option.

The following command will search the url_list.json file for every url linked to the "resource_url" key:

::

    alinkcheck -k resource_url url_list.json

TODO
~~~~

- make sure that the parser works correctly.
- support, and test, more filetypes.

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
