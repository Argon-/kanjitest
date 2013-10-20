#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# This file is part of kanjitest
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


def get_db():
    import sys
    import sqlite3
    try:
        import json
    except ImportError:
        import simplejson as json

    try:
        loc = sys.argv[1]
    except (NameError, IndexError):
        print('No filename given, asuming "db/kanji.db"')
        loc = 'db/kanji.db'


    sqlite3.register_converter("JSON", json.loads)
    conn = sqlite3.connect(loc, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.row_factory = sqlite3.Row

    c.execute('PRAGMA foreign_keys = ON')
    conn.commit()
    return conn, c
