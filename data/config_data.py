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

from collections import OrderedDict


default_settings = OrderedDict()
default_settings['default'] = {
                        'choice'         : None,
                        'choice_example' : ['genki1=1:20', 'genki2=2:10'],
                        'prompt_list'    : 'meaning',
                        'p_min'          : 4,
                        'p_max'          : 100,
                        'exp'            : 4,
                        'permutation'    : False,
                        'prio_proceed'   : False,
                        'db'             : 'kanji.db',
                        'lang'           : 'en',
                        'keymap'         : 'urwid',
                        'ui_class'       : 'urwid',
                        'print_selected' : False,
                        'low_mem'        : False,
                        'verbosity'      : 1,
                        'quiet'          : False,
                        'exit'           : False,
                        'keydebug'       : False,
                        'no_scheck'      : False,
                        }



default_maps = OrderedDict()
default_maps['default'] = {
                        'exit'    : ['esc', 'q'],
                        'skip'    : ['s'],
                        'proceed' : ['up', 'mouse_click_left', 'mouse_click'],
                        'hide'    : ['down'],
                        'prioritylist' : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                        'inc_priority' : ['+'],
                        'dec_priority' : ['-'],
                        }
default_maps['urwid']   = {
                        'exit'    : ['esc', 'q'],
                        'skip'    : ['s'],
                        'proceed' : ['up', 'mouse_click_left', 'mouse_click'],
                        'hide'    : ['down'],
                        'prioritylist' : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                        'inc_priority' : ['+'],
                        'dec_priority' : ['-'],
                        }

default_captions = OrderedDict()
default_captions['en'] = {
                        'header_text'  : 'Prompt for: ',
                        'flipcount'    : '(flips)',
                        'cb_on'        : 'on reading',
                        'cb_kun'       : 'kun reading',
                        'cb_sign'      : 'sign',
                        'cb_meaning'   : 'meaning',
                        'cb_misc'      : 'miscellaneous',
                        'label_sign'   : '',
                        'label_on'     : '▷  ',
                        'label_kun'    : '►  ',
                        'label_meaning': '',
                        'label_misc'   : '',
                        'startup_sign' : '漢字',
                        'startup_msg'  : 'Start with any key',
                        'footer_prio'  : 'Priority: {priority}',
                        'footer_desc'  : 'set priority: `{prioritymin}`-`{prioritymax}`   next: `{proceed}`   skip: `{skip}`',
                        'label_sign_suffix'   : '',
                        'label_on_suffix'     : '',
                        'label_kun_suffix'    : '',
                        'label_meaning_suffix': '',
                        'label_misc_suffix'   : '',
                        }
default_captions['de'] = {
                        'header_text'  : 'Zeige: ',
                        'flipcount'    : '(flips)',
                        'cb_on'        : 'On Lesung',
                        'cb_kun'       : 'Kun Lesung',
                        'cb_sign'      : 'Zeichen',
                        'cb_meaning'   : 'Bedeutung',
                        'cb_misc'      : 'Weiteres',
                        'label_sign'   : '',
                        'label_on'     : '▷  ',
                        'label_kun'    : '▶  ',
                        'label_meaning': '',
                        'label_misc'   : '',
                        'startup_sign' : '漢字',
                        'startup_msg'  : 'Beginne mit beliebiger Taste',
                        'footer_prio'  : 'Priorität: {priority}',
                        'footer_desc'  : 'Priorität setzen: `{prioritymin}`-`{prioritymax}`   Weiter: `{proceed}`   Überspringen: `{skip}`',
                        'label_sign_suffix'   : '',
                        'label_on_suffix'     : '',
                        'label_kun_suffix'    : '',
                        'label_meaning_suffix': '',
                        'label_misc_suffix'   : '',
                        }
