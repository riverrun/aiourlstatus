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
import json

class GetUrls(object):
    """Get the urls from the text file. If it is a json file and a key is provided,
    try to parse as a json file. If the key cannot be found, fallback
    to parsing it as a text file. Text files are parsed using regular expressions.
    """
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
        """Parse the dictionary, or list, in the json file."""
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
        """Create a dictionary for each domain."""
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
        """Sort the list of urls for each domain (most urls first).
        This is so that we can limit the simultaneous requests to each domain.
        """
        self.len_urls = length
        url_dict = self.create_dict()
        self.urls = list(url_dict.values())
        self.urls.sort(key=lambda x: len(x), reverse=True)
