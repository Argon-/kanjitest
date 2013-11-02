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

import abc


def do_nothing(*args, **kwargs):
    pass

class UIException(Exception):
    pass



class Meta_UI_Controller(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def __init__(self, keymap, translate):
        '''
        Create a new instance with the following required arguments:
        keymap    -- function returning a string list value for a given string key
        translate -- function returning a string value for a given string key
                     (might require additional keyword arguments)
        '''
        pass


    @abc.abstractmethod
    def initialize(self, colors=16, palette=None, static_sign_labels=True, div1 = 1, div2 = 1, div3 = 3):
        '''
        Initialize an interface session with various optional keyword arguments:
        colors             -- number of colors support (default: 16)
                              (only useful for text-based user interfaces)
        palette            -- a color palette for text & background colors and 
                              other styling attributes
        static_sign_labels -- display these labels even though the embraced text 
                              is invisible (default: True)
        div1               -- height of text divider #1 (default: 1)
        div2               -- height of text divider #2 (default: 1)
        div3               -- height of text divider #3 (default: 3)
        '''
        pass


    @abc.abstractmethod
    def run(self):
        '''
        Start the UI main loop.
        '''
        pass


    @abc.abstractmethod
    def free(self):
        '''
        Stop the UI main loop and perform clean-up operations.
        '''
        pass


    @abc.abstractmethod
    def redraw(self):
        '''
        Redraw the current screen.
        '''
        pass


    @abc.abstractmethod
    def register_callbacks(self, log=do_nothing, input_handler=do_nothing):
        '''
        Register various callback functions.
        log           -- function taking a log message and an optional `error` boolean
        input_handler -- function taking the invoked user interaction
                         (e.g. a pressed key) as string
        '''
        pass


    @abc.abstractmethod
    def is_key(self, key, action):
        '''
        Return a boolean indicating whether the given `key` is associated with
        the given `action`.
        This allows the UI to use an internal representation for `key`.
        '''
        pass


    @abc.abstractmethod
    def set_initial_visibility(self, *args):
        '''
        Set the intial visibility for every given argument to `True`.
        '''
        pass


    @abc.abstractmethod
    def reveal_current_sign(self):
        '''
        Display every value for the current sign.
        '''
        pass


    @abc.abstractmethod
    def display_sign(self, d, p):
        '''
        Display a new sign and its priority, adhering to the current visibility settings.
        d -- sign data in a dict
        p -- priority for this sign
        '''
        pass


    @abc.abstractmethod
    def set_flips(self, flips):
        '''
        Set the number of flips (a value provided by LDRand).
        '''
        pass


    @abc.abstractmethod
    def set_priority(self, priority):
        '''
        Set the priority. 
        '''
        pass

    @abc.abstractmethod
    def set_set_size(self, size):
        '''
        Set the kanji list's size.
        '''
        pass

    @abc.abstractmethod
    def to_priority(self, key=None):
        '''
        Return the priority entered by the user.
        In most cases the priority might be encoded within a keypress event, so
        supply it as optional argument.
        '''
        pass
