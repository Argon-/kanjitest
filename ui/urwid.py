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

import urwid
from .ui import Meta_UI_Controller
from .ui import do_nothing
from .urwid_data import default_palette


def do_nothing(*args, **kwargs):
    pass


class UI_Controller(Meta_UI_Controller):

    def __init__(self, keymap, translate):
        self.keys = keymap
        self.tr = translate
        self.register_callbacks()
        self.static_labels = True

        self.screen = None
        self.main_loop = None

        self.body_pile = None
        self.footer_columns = None
        
        # currently not needed during runtime
        #self.frame = None
        #self.header = None
        #self.body = None
        #self.footer = None

        self.pile_related_data = dict()


    def init_screen(self, colors, palette=default_palette):
        self.screen = urwid.raw_display.Screen()
        self.screen.set_terminal_properties(colors)
        self.screen.register_palette(palette)


    def initialize(self, colors=16, palette=default_palette, static_sign_labels=True, div1 = 2, div2 = 2, div3 = 4):
        div1, div2, div3 = div1-1, div2-1, div3-1
        self.static_labels = static_sign_labels
        self.init_screen(colors, palette)

        def wrap_attr(widget, attr_map=None, focus_map=None):
            return urwid.AttrMap(widget, attr_map, focus_map)
            
        def create_cb(key, setter, text, state=False):
            cb = urwid.CheckBox(text, state=state, has_mixed=False)
            urwid.connect_signal(cb, 'change', self.checkbox_handler, key)
            self.pile_related_data[key] = [cb, text, setter]
            return wrap_attr(cb, 'checkbox', 'focus')

        self.header_flipcount = urwid.Text(('flipcount', self.tr('flipcount')), align='right')
        header_text = urwid.Text(('header', self.tr('header_text')))

        header_cbs = urwid.Columns([
                                    header_text,
                                    create_cb('on',      self.set_onyomi,  self.tr('cb_on'),      False),
                                    create_cb('kun',     self.set_kunyomi, self.tr('cb_kun'),     False),
                                    create_cb('meaning', self.set_meaning, self.tr('cb_meaning'), False),
                                    create_cb('sign',    self.set_sign,    self.tr('cb_sign'),    False),
                                    create_cb('misc',    self.set_misc,    self.tr('cb_misc'),    False),
                                    self.header_flipcount,
                                    ])

        footer_desc = urwid.Text(('footer_desc', self.tr('footer_desc', 
                                                    prioritymin=self.keys('prioritylist')[0], 
                                                    prioritymax=self.keys('prioritylist')[-1], 
                                                    proceed=self.keys('proceed')[0], 
                                                    skip=self.keys('skip')[0])),
                                                    align='center')
        self.footer_columns = urwid.Columns([
                        ('weight', 1, urwid.Text(('footer_prio', self.tr('footer_prio', priority='-')), align='left')),
                        ('weight', 1, footer_desc),
                        ('weight', 1, urwid.Text(('footer_desc', ' ' * len(self.tr('footer_prio', priority='0'))), align='right')),
                       ], dividechars=2, min_width=len(self.tr('footer_prio', priority='0')))

        self.body_pile = urwid.Pile([
                        ('weight', 1, urwid.Text(('body_sign',     self.tr('startup_sign')),   align='center')),
                        ('weight', 1, urwid.Divider(div_char=u' ', top=div1, bottom=0)),
                        ('weight', 1, urwid.Text(('body_on',       '   '),   align='center')),
                        ('weight', 1, urwid.Text(('body_kun',      '   '),   align='center')),
                        ('weight', 1, urwid.Divider(div_char=u' ', top=div2, bottom=0)),
                        ('weight', 1, urwid.Text(('body_meaning',  self.tr('startup_msg')),   align='center')),
                        ('weight', 2, urwid.Divider(div_char=u' ', top=div3, bottom=0)),
                        ('weight', 1, urwid.Text(('body_misc',     '   '),   align='center')),
                       ])
        body_fill = urwid.Filler(self.body_pile, valign='middle')


        header = wrap_attr(header_cbs,  'header_bg', None)
        body   = wrap_attr(body_fill,   'body_bg',   None)
        footer = wrap_attr(self.footer_columns, 'footer_bg', None)

        frame = urwid.Frame(body=body, header=header, footer=footer, focus_part='header')
        self.main_loop = urwid.MainLoop(frame, screen=self.screen, unhandled_input=self.input_handler)


    def run(self):
        self.main_loop.run()


    def free(self):
        raise urwid.ExitMainLoop()


    def set_initial_visibility(self, *args):
        for i in args:
            if i in self.pile_related_data:
                self.pile_related_data[i][0].set_state(True, do_callback=False)


    def checkbox_handler(self, cb, state, key):
        if key in self.pile_related_data:
            self.pile_related_data[key][0].set_state(state, do_callback=False)
            self.pile_related_data[key][2](self.pile_related_data[key][1])


    def reveal_current_sign(self):
        for i in self.pile_related_data.values():
            _, text, f = i
            f(text, force_reveal=True)


    def register_callbacks(self, log=do_nothing, input_handler=do_nothing):
        self.log = log
        self.input_handler = input_handler


    def is_key(self, key, action):
        # key is a 4-tuple in case of some mouse events
        # translate to a regular key-event
        if len(key) is 4:
            if key[0] == 'mouse press':
                if int(key[1]) is 1:
                    key = 'mouse_click_left'
                elif int(key[1]) is 3:
                    key = 'mouse_click_right'
                else:
                    key = 'mouse_click'
            elif key[0] == 'mouse release':
                if int(key[1]) is 1:
                    key = 'mouse_release_left'
                elif int(key[1]) is 3:
                    key = 'mouse_release_right'
                else:
                    key = 'mouse_release'          # generic mouse release
            elif key[0] == 'mouse drag':
                key = 'mouse_drag'
        
        if key in self.keys(action):
            return True
        return False


    def display_sign(self, d, p):
        # Change hard coded strings below with caution - they're all fullwidth characters.
        # Needed because len() counts a char as 1, disregarding its width. 
        # Since we're padding fullwidth chars, we better padd with fullwidth too.
        # TODO: get rid of hardcoded strings
        def j(d, sep = '、'):
            return sep.join([i for i in d if bool(i)])

        def padd(s1, s2):
            m = max(len(s1), len(s2))
            return (s1 + ('　' * (m - len(s1))), s2 + ('　' * (m - len(s2))))

        self.set_priority(p)
        self.set_sign(j(d['sign']))
        self.set_onyomi(padd(j(d['on']), j(d['kun']))[0])
        self.set_kunyomi(padd(j(d['on']), j(d['kun']))[1])
        self.set_meaning(j(d['meaning'], '; '))
        self.set_misc(j(d['misc'], '; '))


    def __set_footer_columns_content(self, id, attr_map, text, alignment):
        try:
            self.footer_columns.contents[id] = (urwid.Text((attr_map, text), align=alignment), self.footer_columns.options('weight', 1))
        except IndexError:
            pass


    def __set_body_pile_content(self, id, attr_map, text, alignment):
        try:
            self.body_pile.contents[id] = (urwid.Text((attr_map, text), align=alignment), self.body_pile.options('weight', 1))
        except IndexError:
            pass


    def set_sign(self, text, alignment='center', force_reveal=False):
        self.pile_related_data['sign'][1] = text
        t = ''
        if self.static_labels:
            t += self.tr('label_sign')
        if self.pile_related_data['sign'][0].state or force_reveal:
            t += text
        if self.static_labels:
            t += self.tr('label_sign_suffix')
        self.__set_body_pile_content(0, 'body_sign', t, alignment)


    def set_onyomi(self, text, alignment='center', force_reveal=False):
        self.pile_related_data['on'][1] = text
        t = ''
        if self.static_labels:
            t += self.tr('label_on')
        if self.pile_related_data['on'][0].state or force_reveal:
            t += text
        if self.static_labels:
            t += self.tr('label_on_suffix')
        self.__set_body_pile_content(2, 'body_on', t, alignment)


    def set_kunyomi(self, text, alignment='center', force_reveal=False):
        self.pile_related_data['kun'][1] = text
        t = ''
        if self.static_labels:
            t += self.tr('label_kun')
        if self.pile_related_data['kun'][0].state or force_reveal:
            t += text
        if self.static_labels:
            t += self.tr('label_kun_suffix')
        self.__set_body_pile_content(3, 'body_kun', t, alignment)


    def set_meaning(self, text, alignment='center', force_reveal=False):
        self.pile_related_data['meaning'][1] = text
        t = ''
        if self.static_labels:
            t += self.tr('label_meaning')
        if self.pile_related_data['meaning'][0].state or force_reveal:
            t += text
        if self.static_labels:
            t += self.tr('label_meaning_suffix')
        self.__set_body_pile_content(5, 'body_meaning', t, alignment)


    def set_misc(self, text, alignment='center', force_reveal=False):
        self.pile_related_data['misc'][1] = text
        t = ''
        if self.static_labels:
            t += self.tr('label_misc')
        if self.pile_related_data['misc'][0].state or force_reveal:
            t += text
        if self.static_labels:
            t += self.tr('label_misc_suffix')
        self.__set_body_pile_content(7, 'body_misc', t, alignment)


    def set_flips(self, flips):
        self.header_flipcount.set_text(('flipcount', '(' + str(flips) + ')'))


    def set_priority(self, priority):
        self.__set_footer_columns_content(0, 'footer_prio', self.tr('footer_prio', priority=str(priority)), 'left')


    def to_priority(self, key):
        if not key:
            return -999                 # TODO: get rid of magic number
        return int(key)


    def redraw(self):
        self.main_loop.draw_screen()
