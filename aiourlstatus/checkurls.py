# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple text analysis tool
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

import asyncio
import aiohttp
import re
from collections import namedtuple
from itertools import groupby
from urllib.parse import urlparse

def find_urls(data):
    """Extract urls from the data."""
    urls = re.findall('https?://[^\s<>\'"]+', data)
    data = [(urlparse(url).hostname, url) for url in urls]
    data.sort(key=lambda x: x[0])
    urllists = [[g[1] for g in group] for key, group in groupby(data, lambda x: x[0])]
    len_urls = len(urls)
    return urllists, len_urls

def file_check(fname, parse=False):
    """Find urls in a text file and then check those links."""
    print('Parsing the file {}...'.format(fname))
    with open(fname) as f:
        data = f.read()
    stream_check(data, fname, parse)

def stream_check(data, fname='text', parse=False):
    """Find the urls in a text stream and then check these urls."""
    urls, len_urls = find_urls(data)
    if parse or not urls:
        print(urls)
        return
    run_check(fname, urls, len_urls)

async def fetch(session, urllist):
    """Fetch url information for each url within a single domain."""
    sem = asyncio.Semaphore(5)
    for url in urllist:
        with aiohttp.Timeout(30, loop=session.loop):
            try:
                async with sem, session.head(url, allow_redirects=True) as response:
                    await response.release()
            except Exception as e:
                return Result(url, None, None, type(e).__name__)
    return Result(url, response.status, response.history, None)

async def fetch_all(loop, urls):
    """Check all links."""
    Result = namedtuple('Result', 'url status history error')
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(session, urllist, Result) for urllist in urls],
            return_exceptions=True)
        return results

def run_check(fname, urls, len_urls):
    """Run asyncio loop and then print out a report."""
    print('Checking {} links...'.format(len_urls))
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fetch_all(loop, urls))
    report(results)

def report(results):
    """Print out report."""
    res_dict = {'ok': [], 'redirect': [], 'problem': [], 'error': []}
    for res in results:
        if res.status:
            if res.status < 300:
                if res.history:
                    res_dict['redirect'].append((res.url, res.status))
                else:
                    res_dict['ok'].append((res.url, res.status))
            else:
                res_dict['problem'].append((res.url, res.status))
        else:
            res_dict['error'].append((res.url, res.error))
    print(res_dict)
