#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# This file is part of kanji_test
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

import os, sys, argparse, locale, signal
from functools import partial
# Use the system default locale.
# UTF8 is required, modify if necessary.
locale.setlocale(locale.LC_ALL, '')

from importlib import import_module
from rand.ldrand import LDRand
from data.kanji_dict import KDict
from data.config import Config
from data.config import Configuration_Exception
from helpers.func import expand_choice
from helpers.func import add_parser_args
from helpers.func import CArgs
from helpers.func import db_list_to_string
from helpers.func import max_priority



####################
# argument parsing #
####################

args = CArgs()
parser = argparse.ArgumentParser(#description='Specify the kanji you want to test.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 add_help=False)
conf = Config(os.path.dirname(os.path.abspath( __file__ )) + os.sep + 'config.json')

add_parser_args(parser, conf)
parser.parse_args(namespace=args)

conf.language = args.lang
conf.keymap = args.keymap

if args.permutation:
    args.exp = 0
if args.quiet:
    args.verbosity = -1
if not os.path.isfile(args.db):
    print('[db] Error: no file found for: ' + str(args.db))
    sys.exit(1)

args.choice = expand_choice(args.choice)
UI_Controller = getattr(import_module('ui.' + args.ui_class), 'UI_Controller')



##########################
# gather requested kanji #
##########################

k = KDict(args.db)
l = []

args.verbosity > 1 and print('[args] ' + str(args.choice))

if args.choice is None:
    l = k.select_all_keyonly(args.p_min, args.p_max) if args.low_mem else k.select_all(args.p_min, args.p_max)
else:
    for d in args.choice:
        if args.low_mem:
            l += k.select_keyonly(d['book'], d['from'], d['to'], args.p_min, args.p_max)
        else:
            l += k.select(d['book'], d['from'], d['to'], args.p_min, args.p_max)

if args.print_selected:
    if args.low_mem:
        args.verbosity > 0 and print(os.linesep.join(['book: ' + book + ' \tid: ' + str(kid) for book, kid in l]))
    else:
        args.verbosity > 0 and print(db_list_to_string(l))


################
# control flow #
################

rnd = LDRand(len(l), args.exp)


def sign(ui=None, new=False, seed=None):
    new and rnd.next()

    if args.low_mem:
        s = k.select_one(*l[rnd.current])
    else:
        if seed:
            l[rnd.current] = seed
        s = l[rnd.current]

    if ui:
        ui.display_sign(KDict.extract_dict(s), KDict.extract_priority(s))
        ui.set_flips(rnd.flips)
    return s


def reveal_or_next(ui, force=False, go_back=False):
    if go_back:
        reveal_or_next.revealed = False
        sign(ui, new=False)
    elif reveal_or_next.revealed or force:       # next
        reveal_or_next.revealed = False
        sign(ui, new=True)
    else:                                        # reveal
        reveal_or_next.revealed = True
        ui.reveal_current_sign()

reveal_or_next.revealed = False


def update_priority(ui, p_new):
    ui.set_priority(p_new)
    k.update_p(KDict.extract_book(sign()), KDict.extract_id(sign()), p_new)
    sign(seed=KDict.update_priority(sign(), p_new))


def input_handler(ui, key):
    if rnd.current is None and not ui.is_key(key, 'exit'):
        reveal_or_next(ui, force=True)           # start no matter what key was pressed (except exit)
        return                                   # ignore the key

    if ui.is_key(key, 'exit'):
        ui.free()
    elif ui.is_key(key, 'prioritylist'):         # set prio
        if ui.to_priority(key) is KDict.extract_priority(sign()):
            pass
        else:
            p_new = ui.to_priority(key)
            update_priority(ui, p_new if args.no_scheck or (p_new < 100 and p_new > -100) else KDict.extract_priority(sign()))
        if args.prio_proceed:
            reveal_or_next(ui)
    elif ui.is_key(key, 'inc_priority'):
        p_old = KDict.extract_priority(sign())
        p_scheck = (p_old + 1) if args.no_scheck or (p_old + 1) < 100 else 100
        if p_old is not p_scheck:
            update_priority(ui, p_scheck)
        if args.prio_proceed:
            reveal_or_next(ui)
    elif ui.is_key(key, 'dec_priority'):
        p_old = KDict.extract_priority(sign())
        p_scheck = (p_old - 1) if args.no_scheck or (p_old - 1) > -100 else -100
        if p_old is not p_scheck:
            update_priority(ui, p_scheck)
        if args.prio_proceed:
            reveal_or_next(ui)
    elif ui.is_key(key, 'proceed'):              # reveal or next sign
        reveal_or_next(ui)
    elif ui.is_key(key, 'hide'):
        reveal_or_next(ui, go_back=True)
    elif ui.is_key(key, 'skip'):                 # next sign
        reveal_or_next(ui, force=True)
    
    if args.keydebug:
        args.verbosity > 0 and print('[keydebug] ' + str(key))
    else:
        ui.redraw()



#############
# main loop #
#############

args.exit and sys.exit(0)
ui = UI_Controller(keymap=conf.get_key, translate=conf.get_translation)

try:
    signal.signal(signal.SIGINT, lambda x,y: ui.free())

    ui.register_callbacks(input_handler=partial(input_handler, ui))
    ui.initialize(colors=256)
    ui.set_initial_visibility(*args.prompt_list)
    ui.run()
except Exception as e:
    args.verbosity > 0 and print('[main] Error: ' + str(e))
    ui.free()
