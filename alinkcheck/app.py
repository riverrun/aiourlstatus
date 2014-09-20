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

import re
import click
from .checkurls import CheckLinks

class GetUrls(object):
    """Find all the urls in the text and create a dictionary for each domain."""
    def __init__(self, data):
        self.sort_list(re.findall('https?://[^\s<>\'"]+', data))

    def create_dict(self, urls):
        """Create a dictionary for each domain."""
        url_dict = {}
        for url in urls:
            try:
                temp_key = url.split('/')[2]
            except Exception:
                temp_key = url
            if temp_key.startswith('www.'):
                key = temp_key.split('.', 1)[1]
            else:
                key = temp_key
            if key in url_dict:
                url_dict[key].append(url)
            else:
                url_dict[key] = [url]
        return url_dict

    def sort_list(self, urls):
        """Sort the list of urls for each domain (most urls first).
        This is so that we can limit the simultaneous requests to each domain.
        """
        self.len_urls = len(urls)
        url_dict = self.create_dict(urls)
        self.urls = list(url_dict.values())
        self.urls.sort(key=lambda x: len(x), reverse=True)

@click.command()
@click.argument('filename', nargs=-1)
@click.option('--parse/--no-parse', '-p', default=False,
        help='Just parse the json / text files and then exit.')
@click.option('--verbose', '-v', default=False, count=True,
        help='v will show the redirected links and vv will also print out the links that are OK.')
def cli(filename, parse, verbose):
    """FILENAME is the file(s) which you want checked. It can be json or
    any other text format, and alinkcheck should be able to find the links in it.
    Then all the links will be checked and a report will be printed out to console."""
    verb_redir = True if verbose else False
    verb_ok = True if verbose > 1 else False
    for fname in filename:
        print('Parsing the file {}...'.format(fname))
        with open(fname) as f:
            data = f.read()
        g = GetUrls(data)
        if parse or not g.urls:
            print(g.urls)
            continue
        cl = CheckLinks(fname, g.urls, g.len_urls, verb_redir, verb_ok)
        cl.run_check()
    click.secho('See you later.', fg='yellow')
