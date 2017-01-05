# Authors: David Whitlock <alovedalongthe@gmail.com>
# A tool for testing url links
# Copyright (C) 2014-2017 David Whitlock
#
# Aiourlstatus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Aiourlstatus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Aiourlstatus.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import argparse
import re
from .checkurls import file_check

usage = """filename is the file(s) which you want checked. It can be json, xml or
    any other text format, and aiourlstatus will be able to find the links in it.\n
    Then all the links will be checked and a report will be printed out to console.\n
    By default, the report will just list those urls with problems (client or server
    errors) and urls with other errors. If you want the urls that were redirected
    to be printed out, use the verbose option. If you also want the urls that were
    OK to be printed out, use the double verbose (-vv) option."""

def cli():
    parser = argparse.ArgumentParser(description='Asynchronous link checker', prog='aiourlstatus', epilog=usage)
    parser.add_argument('filename', nargs='+', help='the text file which contains the urls')
    parser.add_argument('-t', '--timeout', type=int, nargs='?', help='set request timeout')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose')
    args = parser.parse_args()
    for fname in args.filename:
        file_check(fname, args.verbose, args.timeout)
