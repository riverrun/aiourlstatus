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

import asyncio
import aiohttp
import click

class CheckLinks(object):
    """Check the links found in the text file."""
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
        self.headers = {'User-Agent':
                'aiourlstatus/0.3.3 (https://github.com/riverrun/aiourlstatus/)'}

    def run_check(self):
        """Set up loop and run async checks."""
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
        """A limit is placed on urls in each separate domain."""
        sem = asyncio.Semaphore(5)
        for url in urllist:
            with (yield from sem):
                yield from self.check_url(url)

    def check_url(self, arg):
        """Check url and add to ok, redirects, problems, or errors list."""
        try:
            resp = yield from aiohttp.request('HEAD', arg,
                    allow_redirects=False, headers=self.headers)
            if 301 <= resp.status <= 308:
                redirects = 0
                while redirects < 5:
                    new_url = resp.headers.get('LOCATION') or resp.headers.get('URI')
                    resp = yield from aiohttp.request('HEAD', new_url,
                            allow_redirects=False, headers=self.headers)
                    if 200 <= resp.status <= 208:
                        if self.verb_redir:
                            self.redirects.append('{} redirected to {}'.format(arg, new_url))
                        break
                    else:
                        redirects += 1
            elif 200 <= resp.status <= 208:
                if self.verb_ok:
                    self.oks.append('{} {}'.format(arg, resp.status))
            else:
                self.probs.append('{} {}'.format(arg, resp.status))
        except Exception as e:
            self.errors.append('{} {}'.format(arg, e))

    def report(self):
        """Print out report."""
        if self.oks:
            click.secho('The following links are OK:', fg='yellow')
            print('\n'.join(self.oks))
        if self.redirects:
            click.secho('\nThe following links have been redirected:', fg='yellow')
            print('\n'.join(self.redirects))
        if self.probs:
            click.secho('\nThere were problems with these links:', fg='red')
            print('\n'.join(self.probs))
        if self.errors:
            click.secho('\nThere were errors with these links:', fg='red')
            print('\n'.join(self.errors))
        click.secho('{}: total {} links, could not connect to {} links.'.format(self.fname,
            self.len_urls, len(self.probs) + len(self.errors)), fg='yellow')
