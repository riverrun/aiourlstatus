# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple text analysis tool
# Copyright (C) 2014 David Whitlock
#
# Alinkcheck is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alinkcheck is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Alinkcheck.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import click
from .findurls import GetUrls
from .checkurls import CheckLinks

@click.command()
@click.argument('filename', nargs=-1)
@click.option('--keyname', '-k', default=None,
        help='Name of the key for each url in the json file / dictionary.')
@click.option('--parse/--no-parse', '-p', default=False,
        help='Just parse the json / text files and then exit.')
@click.option('--verbose', '-v', default=False, count=True,
        help='v will show the redirected links and vv will also print out the links that are OK.')
def cli(filename, keyname, parse, verbose):
    """FILENAME is the file(s) which you want checked. It can be json or
    any other text format, and alinkcheck should be able to find the links in it.
    Then all the links will be checked and a report will be printed out to console."""
    verb_redir = True if verbose else False
    verb_ok = True if verbose > 1 else False
    click.clear()
    for fname in filename:
        print('Parsing the file {}...'.format(fname))
        g = GetUrls(fname, keyname)
        if parse or not g.urls:
            print(g.urls)
            continue
        cl = CheckLinks(fname, g.urls, g.len_urls, verb_redir, verb_ok)
        cl.run_check()
    click.secho('See you later.', fg='yellow')
