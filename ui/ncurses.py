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

import curses
from .ui import Meta_UI


# code here is (was) mainly for testing and serves no real purpose

class UI_Controller(Meta_UI_Controller):

    def __init__(self):
        super(Curses, self).__init__()
        self.stdscr = None
        self.top = None
        self.bot = None
        self.mid = None
        self.mid_center = None


    def initialize(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        #curses.curs_set(0)
        self.stdscr.keypad(1)
        self.create_windows()


    def free(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def addstr(self, s):
        self.stdscr.addstr(s.encode('utf8'))

    def getch(self):
        return self.stdscr.getch()


    def create_windows(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.top = self.stdscr.subwin(1, self.stdscr.getmaxyx()[0], 0, 0)
        self.top.bkgdset(ord('x'), curses.color_pair(1))


    def test(self):
        # self.stdscr.getmaxyx()[0] 
        self.top.addstr('aaaaaaaaaaaaaaaaaa')
        #self.stdscr.addstr('bbbbb')
        self.top.refresh()
        self.stdscr.refresh()

        self.stdscr.move(self.stdscr.getmaxyx()[0]-1, self.stdscr.getmaxyx()[1]-1)
        self.getch()
