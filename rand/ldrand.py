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

import random


class LDRand(object):

    def __init__(self, length, exp = 6, init_dist = None, debug = False):
        self.__len = length
        self.__exp = exp
        self.__debug = debug
        self.__base = 2
        self.__flips = 0
        self.__dist_max = self.__base ** self.__exp
        self.__log = ''
        self.__current = None

        if init_dist:
            self.__dist = init_dist
            self.__len = len(init_dist)
            self.__dist_max = max(self.__dist)
        else:
            self.__dist = [self.__base**self.__exp] * self.__len

        if self.__len < 2:
            raise ValueError('Doesn\'t make much sense to choose from less than 2 elements')


    def next(self):
        cd = random.randint(0, sum(self.__dist) - 1)
        dist_old = str(self.__dist)

        for i in range(self.__len):
            cd -= self.__dist[i]

            if cd < 0:
                self.__dist[i] //= self.__base
                new_max = max(self.__dist)
                if new_max < self.__dist_max:
                    self.__dist_max = new_max * self.__base if new_max > 0 else 1
                    self.__dist = [n * self.__base if n > 0 else 1 for n in self.__dist]
                    self.__flips += 1
                if self.__debug:
                    self.__log = 'old: ' + dist_old + '\nnew: ' + str(self.__dist) + '\ni = ' + str(i) + '\n'
                self.__current = i
                return i
        raise ValueError('Reached end of function without generating a proper return value. Seems like next()\'s invariant is a bit more variant than expected')


    def get_log(self):
        return self.__log

    def get_flips(self):
        return self.__flips

    def get_current_index(self):
        return self.__current

    log = property(get_log)
    flips = property(get_flips)
    current = property(get_current_index)
