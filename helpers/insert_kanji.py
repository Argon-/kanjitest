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

import os
import sys
import locale

# Necessary to bypass 'no relativ imports from within moduls' in py3...
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import data.kanji_dict as kanjidict


# Use the system default locale.
# UTF8 is required, modify if necessary.
locale.setlocale(locale.LC_ALL, '')

try:
    loc = sys.argv[1]
except (NameError, IndexError):
    print('No filename given, asuming "db/kanji.db"')
    loc = 'db/kanji.db'


# some samples

prio = 4

l = [ \
['genki1',   1, prio, dict(sign = u'一', 
                           on = [u'いち', u'いっ'], 
                           kun = [u'ひと'], 
                           meaning = [u'one'], 
                           misc = ['tttttt'])], 

['genki1',   2, prio, dict(sign = u'二', 
                           on = [u'に'], 
                           kun = [u'ふた'], 
                           meaning = [u'two'], 
                           misc = ['tttttt'])], 

['genki1',   3, prio, dict(sign = u'三', 
                           on = [u'さん'], 
                           kun = [u'みっ'], 
                           meaning = [u'three'], 
                           misc = ['tttttt'])], 

['genki1',   4, prio, dict(sign = u'四', 
                           on = [u'し'], 
                           kun = [u'よん', u'よ', u'よっ'], 
                           meaning = [u'four'], 
                           misc = ['tttttt'])], 

['genki1',  30, prio, dict(sign = u'山', 
                           on = [u'さん'], 
                           kun = [u'やま'], 
                           meaning = [u'mountain'], 
                           misc = ['tttttt'])], 

['genki1',  31, prio, dict(sign = u'川', 
                           on = [], 
                           kun = [u'かわ', u'がわ'], 
                           meaning = [u'river'], 
                           misc = ['tttttt'])], 

['genki1',  32, prio, dict(sign = u'元', 
                           on = [u'げん', u'がん'], 
                           kun = [u'もと'], 
                           meaning = [u'origin'], 
                           misc = ['tttttt'])], 

['genki1',  33, prio, dict(sign = u'気', 
                           on = [u'き'], 
                           kun = [], 
                           meaning = [u'spirit'], 
                           misc = ['tttttt'])], 
]


with kanjidict.KDict(loc) as k:
    for i in l:
        print('Inserting:', i)
        book, kid, p, d = i
        k.insert(book = book, kid = kid, d = d, p = p)
    k.commit()
