#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# This file is part of REPLACEME
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
import argparse
import re


class CArgs(object):
    pass


def set_argument(arg):
    try:
        return re.match(r'^[a-zA-Z0-9_]+(=\d+:\d+)*$', arg).group(0)
    except:
        raise argparse.ArgumentTypeError('value `{s}` does not match the required format'.format(s=arg))


def prompt_argument(arg):
    try:
        return [i.strip() for i in re.match(r'^(sign|on|kun|meaning|misc)(,[ ]*(sign|on|kun|meaning|misc))*$', arg).group(0).split(',')]
    except:
        raise argparse.ArgumentTypeError('value `{s}` does not match the required format'.format(s=arg))


def expand_choice(choice):
    l = []
    if not choice or None in choice:
        return None
    for bookstr in choice:
        if ':' not in bookstr:
            l += [{'book': bookstr, 'from': 0, 'to': max_priority()}]
        else:
            book, rest = bookstr.split('=', 1)
            for rs in rest.split('='):
                l += [{'book': book, 'from': int(rs.split(':', 1)[0]), 'to': int(rs.split(':', 1)[1])}]
    return l


def add_parser_args(parser, c):
    parser.add_argument('--set', '-s', dest='choice', metavar='textbook(=from:to)*',
                    default=c.get('choice', None), action='append', type=set_argument, required=False,
                    help='Limit the kanji to test. Multiple usage possible.')
    parser.add_argument('--prompt', '-pt',dest='prompt_list', metavar='sign|on|kun|meaning|misc',
                    default=c.get('prompt_list', 'meaning'), action='store', type=prompt_argument, required=False,
                    help='The part(s) of the kanji to be visible. (comma separated list)')
    parser.add_argument('--priority', '-p', dest='p_min', metavar='n',
                    default=c.get('p_min', 4), action='store', type=int, required=False,
                    help='The min required priority for a kanji to be eligible.')
    parser.add_argument('--priority_max', '-pmax', dest='p_max', metavar='n',
                    default=c.get('p_max', max_priority()), action='store', type=int, required=False,
                    help='The max allowed priority for a kanji to be eligible.')
    parser.add_argument('--depth', '-d', dest='exp', metavar='n',
                    default=c.get('exp', 4), action='store', type=int, required=False,
                    help='Specify the `randomness` used for shuffling the kanji. A value of 0 results in a permutation.')
    parser.add_argument('--perm', '-pm',dest='permutation', action='store_true',
                    default=c.get('permutation', False), required=False,
                    help='Alias for --depth 0. (takes precedence)')
    parser.add_argument('--prioproceed', '-pp', dest='prio_proceed', action='store_true',
                    default=c.get('prio_proceed', False), required=False,
                    help='Assigning a priority acts like `proceed`.')
    #parser.add_argument('--profile', '-pr', dest='profile', metavar='myprofile',
    #                default='default', action='store', type=str, required=False,
    #                help='A profile specified in your configuration file.')
    parser.add_argument('--database', '-db', dest='db', metavar='your.db',
                    default=c.get('db', 'kanji.db'), action='store', type=str, required=False,
                    help='The location of your kanji sqlite3 database.')
    #parser.add_argument('--config', '-c', dest='config', metavar='conf.json',
    #                default='', action='store', type=str, required=False,
    #                help='The location of your configuration file in case it\'s in non-default directories.')
    parser.add_argument('--language', '--lang', '-l', dest='lang', metavar='en',
                    default=c.get('lang', 'en'), action='store', type=str, required=False,
                    help='The captions dictionary to load.')
    parser.add_argument('--keymap', '-km', dest='keymap', metavar='default',
                    default=c.get('keymap', 'urwid'), action='store', type=str, required=False,
                    help='The keymap dictionary to load.')
    parser.add_argument('--ui', dest='ui_class', choices=['urwid'],
                    default=c.get('ui_class', 'urwid'), action='store', type=str, required=False,
                    help='The UI module name to load.')
    parser.add_argument('--print', '-prt',dest='print_selected', action='store_true',
                    default=c.get('print_selected', False), required=False,
                    help='Print the selected kanji.')
    parser.add_argument('--small_footprint', '-sp', '-lm', dest='low_mem', action='store_true',
                    default=c.get('low_mem', False), required=False,
                    help='Decrease memory usage. Results in slightly increased load times for displaying a sign.')
    parser.add_argument('--verbose', '-v', dest='verbosity', action='count',
                    default=c.get('verbosity', 1), required=False,
                    help='Print additional output. Use it multiple times to increase the verbosity level.')
    parser.add_argument('--quiet', '-q', dest='quiet', action='store_true',
                    default=c.get('quiet', False), required=False,
                    help='Supress every kind of output except of interpreter messages. (takes precedence)')
    parser.add_argument('--version', '-version', action='version', version='%(prog)s 0.1 dev',
                    help='Show the version number and exit.')
    #parser.add_argument('--no-config', dest='no_config', action='store_true',
    #                default=False, required=False,
    #                help='Load no configuration files, use default values.')
    parser.add_argument('--exit', '-e',dest='exit', action='store_true',
                    default=c.get('exit', False), required=False,
                    help='Quit before entering the UI main loop.')
    parser.add_argument('--debug_key', dest='keydebug', action='store_true',
                    default=c.get('keydebug', False), required=False,
                    help='Print keypress string.')
    parser.add_argument('--help', '-h', action='help',
                    help='Show this help message and exit.')



def db_list_to_string(l):
    s = ''
    for book, kid, d, p in l:
        s += concat_entry(book, kid, d, p)
        s += os.linesep
    return s[0:s.rfind(os.linesep)]

def concat_entry(book, kid, d, p):
    s  = book + u'\t '
    s += str(kid) + u'\t '
    s += str(p) + u'\t '
    
    s += d['sign']
    s += u'  '
    for i in d['on']:
        s += u' ' + i
    s += u'\t '
    for i in d['kun']:
        s += u' ' + i
    s += u'\t '
    for i in d['meaning']:
        s += u' ' + i
    s += u'\t '
    for i in d['misc']:
        s += u' ' + i
    s += u''
    return s

def max_priority():
    return 2**31