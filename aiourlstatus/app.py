# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple text analysis tool
# Copyright (C) 2014 David Whitlock
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

import re
import click
from .checkurls import CheckLinks

def create_dict(urls):
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

def find_sort_urls(data):
    """Sort the list of urls for each domain (most urls first).
    This is so that we can limit the simultaneous requests to each domain.
    """
    urls = re.findall('https?://[^\s<>\'"]+', data)
    len_urls = len(urls)
    url_dict = create_dict(urls)
    urls = list(url_dict.values())
    urls.sort(key=lambda x: len(x), reverse=True)
    return urls, len_urls

def file_check(fname, parse=False, verb_redir=False, verb_ok=False):
    """Open a file and then run the stream_check function."""
    print('Parsing the file {}...'.format(fname))
    with open(fname) as f:
        data = f.read()
    stream_check(data, fname, parse, verb_redir, verb_ok)

def stream_check(data, fname='text', parse=False, verb_redir=False, verb_ok=False):
    """Find the urls in a text stream and then check these urls."""
    urls, len_urls = find_sort_urls(data)
    if parse or not urls:
        print(urls)
        return
    cl = CheckLinks(fname, urls, len_urls, verb_redir, verb_ok)
    cl.run_check()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('filename', nargs=-1)
@click.option('--parse/--no-parse', '-p', default=False,
        help='Just parse the json / text files and then exit.')
@click.option('--verbose', '-v', default=False, count=True,
        help='v will show the redirected links and vv will also print out the links that are OK.')
def cli(filename, parse, verbose):
    """FILENAME is the file(s) which you want checked. It can be json, xml or
    any other text format, and aiourlstatus will be able to find the links in it.\n
    Then all the links will be checked and a report will be printed out to console.\n
    By default, the report will just list those urls with problems (client or server
    errors) and urls with other errors. If you want the urls that were redirected
    to be printed out, use the verbose option. If you also want the urls that were
    OK to be printed out, use the double verbose (-vv) option."""
    verb_redir = True if verbose else False
    verb_ok = True if verbose > 1 else False
    for fname in filename:
        file_check(fname, parse, verb_redir, verb_ok)
    click.secho('See you later.', fg='yellow')
