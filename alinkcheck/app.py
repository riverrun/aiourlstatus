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
    def __init__(self, fname, urls, verb_redir, verb_ok):
        self.oks = []
        self.redirects = []
        self.probs = []
        self.errors = []
        self.fname = fname
        self.urls = urls
        self.verb_redir = verb_redir
        self.verb_ok = verb_ok

    def run_check(self):
        print('Checking {} links...'.format(len(self.urls)))
        loop = asyncio.get_event_loop()
        self.sem = asyncio.Semaphore(100)
        #func = asyncio.wait([self.check_url(url) for url in self.urls])
        func = self.wait_prog([self.check_url(url) for url in self.urls])
        loop.run_until_complete(func)
        self.report()

    @asyncio.coroutine
    def wait_prog(self, coros):
        with click.progressbar(asyncio.as_completed(coros), length=len(coros)) as prog:
            for f in prog:
                yield from f

    @asyncio.coroutine
    def check_url(self, arg):
        try:
            with (yield from self.sem):
                resp = yield from aiohttp.request('HEAD', arg, allow_redirects=not self.verb_redir)
            if self.verb_redir and resp.status in (301, 302):
                resp = yield from aiohttp.request('HEAD', arg, max_redirects=5)
                if resp.status == 200:
                    scheme = arg.split(':', 1)[0] + '://' if arg.startswith('http') else '://'
                    self.redirects.append('{} redirected to {}'.format(arg,
                        ''.join([scheme, resp.host, resp.url])))
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
            click.secho('\nThese links were redirected:', fg='yellow')
            print('\n'.join(self.redirects))
        if self.probs:
            click.secho('\nThere were problems with these links:', fg='red')
            print('\n'.join(self.probs))
        if self.errors:
            click.secho('\nThere were errors with these links:', fg='red')
            print('\n'.join(self.errors))
        click.secho('{}: total {} links, could not connect to {} links.'.format(self.fname,
            len(self.urls), len(self.probs) + len(self.errors)), fg='yellow')

class GetUrls(object):
    def __init__(self, fname):
        self.urls = []
        self.get_ftype(fname)

    def get_ftype(self, fname):
        if fname.endswith('json'):
            self.open_json(fname)
        else:
            self.open_txt(fname)

    def open_json(self, fname):
        with open(fname) as f:
            data = json.load(f)
        self.parse_dict(data)

    def parse_dict(self, data):
        if isinstance(data, dict):
            for key, val in data.items():
                if val.startswith('http'):
                    self.urls.append(val)
                else:
                    self.parse_dict(val)
        elif isinstance(data, list):
            for sub in data:
                if sub.startswith('http'):
                    self.urls.append(sub)
                else:
                    self.parse_dict(sub)

    def open_txt(self, fname):
        with open(fname) as f:
            data = f.read()
        self.urls = re.findall('https?://[^\s<>\'"]+', data)

@click.command()
@click.argument('filename', nargs=-1)
@click.option('--parse/--no-parse', '-p', default=False,
        help='Just parse the json / text files and then exit.')
@click.option('--verbose', '-v', default=False, count=True,
        help='v will check which links were redirected and vv will also print the links that are OK.')
def cli(filename, parse, verbose):
    verb_redir = verbose > 0
    verb_ok = verbose > 1
    for fname in filename:
        print('Parsing the file {}...'.format(fname))
        g = GetUrls(fname)
        if parse:
            print(g.urls)
            continue
        cl = CheckLinks(fname, g.urls, verb_redir, verb_ok)
        cl.run_check()
    click.secho('See you later.', fg='yellow')

if __name__ == '__main__':
    cli()
