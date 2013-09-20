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

import sys
import sqlite3
try:
    import json
except ImportError:
    import simplejson as json


class KDict:

    def __init__(self, filename = 'kanji.db', auto_commit=True, return_updated=False):
        self.filename = filename
        self.autoci = auto_commit
        self.ret_up = return_updated
        sqlite3.register_converter('JSON', lambda n: json.loads(n.decode('utf-8')))

        self.conn = sqlite3.connect(self.filename, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        #self.c.row_factory = sqlite3.Row           # access rows with ['rowname'] notation

        self.c.execute('PRAGMA foreign_keys = ON')
        self.commit()

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.conn.commit()
        self.conn.close()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def __serialize(self, d):
        #return json.dumps(d, ensure_ascii=False)
        return json.dumps(d)

    def commit(self):
        self.conn.commit()

    def close(self, graceful=True):
        graceful and self.conn.commit()
        self.conn.close()

    def insert(self, book, kid, d, p = 3):
        self.c.execute('INSERT INTO kanji VALUES(?, ?, ?, ?)', [kid, book, self.__serialize(d), p])
        self.autoci and self.commit()

    def select(self, book, from_id, to_id, p_min = 0, p_max = 2**31):
        self.c.execute('''SELECT book, id, d, priority FROM kanji
                          WHERE  kanji.book = ?
                          AND    kanji.priority > ?
                          AND    kanji.priority < ?
                          AND    kanji.id < ?
                          AND    kanji.id > ?''', [book, p_min-1, p_max+1, to_id+1, from_id-1])
        return self.c.fetchall()

    def select_keyonly(self, book, from_id, to_id, p_min = 0, p_max = 2**31):
        self.c.execute('''SELECT book, id FROM kanji
                          WHERE  kanji.book = ?
                          AND    kanji.priority > ?
                          AND    kanji.priority < ?
                          AND    kanji.id < ?
                          AND    kanji.id > ?''', [book, p_min-1, p_max+1, to_id+1, from_id-1])
        return self.c.fetchall()

    def select_all(self, p_min = 0, p_max = 2**31):
        self.c.execute('''SELECT book, id, d, priority FROM kanji
                          WHERE  kanji.priority > ?
                          AND    kanji.priority < ?''', [p_min-1, p_max+1])

        return self.c.fetchall()

    def select_all_keyonly(self, p_min = 0, p_max = 2**31):
        self.c.execute('''SELECT book, id FROM kanji
                          WHERE  kanji.priority > ?
                          AND    kanji.priority < ?''', [p_min-1, p_max+1])
        return self.c.fetchall()

    def select_one(self, book, kid):
        self.c.execute('''SELECT book, id, d, priority FROM kanji
                          WHERE  kanji.book = ?
                          AND    kanji.id = ?''', [book, kid])
        return self.c.fetchall()[0]

    def update(self, book, kid, d):
        self.c.execute('''UPDATE kanji
                          SET    d = ?
                          WHERE  kanji.book = ?
                          AND    kanji.id = ?''', [self.__serialize(d), book, kid])
        self.autoci and self.commit()
        if self.ret_up:
            return self.select_one(book, kid)


    def update_p(self, book, kid, p):
        self.c.execute('''UPDATE kanji
                          SET    priority = ?
                          WHERE  kanji.book = ?
                          AND    kanji.id = ?''', [p, book, kid])
        self.autoci and self.commit()
        if self.ret_up:
            return self.select_one(book, kid)

    def delete(self, book, kid):
        self.c.execute('''DELETE FROM kanji
                          WHERE  kanji.book = ?
                          AND    kanji.id = ?''', [book, kid])
        self.autoci and self.commit()

    
    def extract_book(s):
        return s[0]
    def extract_id(s):
        return s[1]
    def extract_dict(s):
        return s[2]
    def extract_priority(s):
        return s[3]
    def update_priority(s, p):
        return (s[0], s[1], s[2], p)
