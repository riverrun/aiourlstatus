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
import asyncio
import json
import click
import aiohttp

class CheckLinks(object):
    def __init__(self, fname, urls, len_urls, verb_redir, verb_ok):
        self.oks = []
        self.redirects = []
        self.probs = []
        self.errors = []
        self.fname = fname
        self.urls = urls
        self.len_urls = len_urls
        self.verb_redir = verb_redir
        self.verb_ok = verb_ok

    def run_check(self):
        print('Checking {} links...'.format(self.len_urls))
        loop = asyncio.get_event_loop()
        func = self.wait_prog([self.check_urllist(urllist) for urllist in self.urls])
        loop.run_until_complete(func)
        self.report()

    def wait_prog(self, coros):
        with click.progressbar(asyncio.as_completed(coros), length=len(coros)) as prog:
            for f in prog:
                yield from f

    @asyncio.coroutine
    def check_urllist(self, urllist):
        sem = asyncio.Semaphore(5)
        for url in urllist:
            with (yield from sem):
                yield from self.check_url(url)

    def check_url(self, arg):
        try:
            resp = yield from aiohttp.request('HEAD', arg, allow_redirects=False)
            if resp.status in (301, 302, 307):
                redirects = 0
                while redirects < 5:
                    new_url = resp.headers.get('LOCATION') or resp.headers.get('URI')
                    resp = yield from aiohttp.request('HEAD', new_url, allow_redirects=False)
                    if resp.status == 200:
                        if self.verb_redir:
                            self.redirects.append('{} redirected to {}'.format(arg, new_url))
                        break
                    else:
                        redirects += 1
            elif resp.status == 200:
                if self.verb_ok:
                    self.oks.append('{} {}'.format(arg, resp.status))
            else:
                self.probs.append('{} {}'.format(arg, resp.status))
        except Exception as e:
            self.errors.append('{} {}'.format(arg, e))

    def report(self):
        if self.oks:
            click.secho('The following links are OK:', fg='yellow')
            print('\n'.join(self.oks))
        if self.redirects:
            click.secho('\nThe following links have been redirected:', fg='yellow')
            print('\n'.join(self.oks))
        if self.probs:
            click.secho('\nThere were problems with these links:', fg='red')
            print('\n'.join(self.probs))
        if self.errors:
            click.secho('\nThere were errors with these links:', fg='red')
            print('\n'.join(self.errors))
        click.secho('{}: total {} links, could not connect to {} links.'.format(self.fname,
            self.len_urls, len(self.probs) + len(self.errors)), fg='yellow')

class GetUrls(object):
    def __init__(self, fname, keyname):
        self.urls = []
        if keyname:
            self.keyname = keyname
            self.get_ftype(fname)
            if self.urls == []:
                print('The keyname seems to be wrong. Parsing as text file.')
                self.open_txt(fname)
        else:
            self.open_txt(fname)
        length = len(self.urls)
        self.sort_list(length)

    def get_ftype(self, fname):
        if fname.endswith('json'):
            self.open_json(fname)
        else:
            self.open_txt(fname)

    def open_json(self, fname):
        with open(fname) as f:
            data = json.load(f)
        try:
            self.parse_dict(data)
        except Exception as e:
            print(e, 'error while parsing json file. Parsing as text file.')
            self.open_txt(fname)

    def parse_dict(self, data):
        if isinstance(data, dict):
            for key, val in data.items():
                if key == self.keyname:
                    self.urls.append(val)
                else:
                    self.parse_dict(val)
        elif isinstance(data, list):
            for sub in data:
                if isinstance(sub, str) and sub.startswith('http'):
                    self.urls.append(sub)
                else:
                    self.parse_dict(sub)

    def open_txt(self, fname):
        with open(fname) as f:
            data = f.read()
        self.urls = re.findall('https?://[^\s<>\'"]+', data)

    def create_dict(self):
        url_dict = {}
        for url in self.urls:
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

    def sort_list(self, length):
        self.len_urls = length
        url_dict = self.create_dict()
        self.urls = list(url_dict.values())
        self.urls.sort(key=lambda x: len(x), reverse=True)

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
