"""aiourlstatus is a tool for checking url links.

It is designed to be used either as a command-line app or in a python shell.

It depends on Python 3.5 as it takes advantage of the async / await syntax.

For information about the command-line options, run
`aiourlstatus -h`.

If you are using this tool in a python shell, the main entry points are the
`file_check` and `stream_check` functions in the checkurls module.
The `file_check` function parses any text file and checks any urls it
finds. The `stream_check` function behaves in the same way, but it
parses a text stream rather than a file.

Examples:

    from aiourlstatus import stream_check

    text = "https://www.python.org and https://www.haskell.org are great"
    stream_check(text)

"""

from .checkurls import file_check
from .checkurls import stream_check
