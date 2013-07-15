#!/usr/bin/python
# -*- coding: utf-8 -*-
###
#
# Copyright (c) 2012 Mehdi Abaakouk <sileht@sileht.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#
###


from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="userbrowser",
    description="Logged user can browse their file",
    long_description=__doc__,
    version="0.1",

    author="Mehdi Abaakouk",
    author_email="sileht@sileht.net",
    url="https://github.com/sileht/python-userbrowser",

    install_requires=required,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ubmanager = userbrowser:ubmanager',
            'ubrunserver = userbrowser:ubrunserver'
        ]
    },
    include_package_data=True,
    packages=['userbrowser'],
    package_data={'userbrowser': ['templates/*',
                                  'schema.sql']},

    platforms='any',
    license="GPL3",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
