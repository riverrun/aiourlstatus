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

from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='aiourlstatus',
    version='0.3.3',
    author='David Whitlock',
    author_email='alovedalongthe@gmail.com',
    url='https://github.com/riverrun/aiourlstatus',
    description='A tool to check links from a json / text file',
    long_description=long_description,
    license='GPLv3',
    packages=['aiourlstatus'],
    include_package_data=False,
    zip_safe=False,
    platforms='any',
    install_requires=['aiohttp', 'click'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
    ],
    entry_points={
        'console_scripts': [
            'aiourlstatus = aiourlstatus.app:cli',
            ]
        },
)
