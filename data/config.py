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

import os
try:
    import json
except ImportError:
    import simplejson as json
from collections import OrderedDict
from .config_data import default_settings
from .config_data import default_captions
from .config_data import default_maps


class Configuration_Exception(Exception):
    pass


class Config(object):

    def __init__(self, conffile, relpath, profile='default', lang='en', keymap = 'default', strict_profile=False, strict_lang=False, strict_keymap=False):
        self.relpath = relpath
        self.conffile = relpath + conffile

        self.default_settings = default_settings
        self.default_captions = default_captions
        self.default_maps = default_maps

        self.settings = default_settings
        self.captions = default_captions
        self.maps = default_maps

        self.strict_profile = strict_profile
        self.strict_lang = strict_lang
        self.strict_keymap = strict_keymap
        self.__load_config()
        self.__set_profile(profile)
        self.__set_lang(lang)
        self.__set_map(keymap)

    
    def __load_config(self):
        c = None
        try:
            c = json.load(open(self.conffile))
            if 'settings' in c:
                self.settings = c['settings']
            else:
                self.get('quiet', False) or print('[config] Warning: no dictionary found for: settings')
            if 'captions' in c:
                self.captions = c['captions']
            else:
                self.get('quiet', False) or print('[config] Warning: no dictionary found for: captions')
            if 'maps' in c:
                self.maps = c['maps']
            else:
                self.get('quiet', False) or print('[config] Warning: no dictionary found for: maps')

            for prf in self.settings:
                if 'db_relative' in self.settings[prf]:
                    self.settings[prf]['db_relative'] = self.relpath + self.settings[prf]['db_relative'] # horrible
        except FileNotFoundError as e:
            self.get('quiet', False) or print('[config] Error: no file found for ' + str(self.conffile))
            self.get('quiet', False) or print('[config] falling back to default values')


    def reload_config(self):
        self.__load_config()
        

    ############
    # settings #
    ############

    def get(self, key, default):
        if key in self.settings[self.profile]:
            return self.settings[self.profile][key]
        elif self.profile in self.default_settings and key in self.default_settings[self.profile]:
            self.get('quiet', False) or print('[config] config specifies no value for key: ' + str(key))
            return self.default_settings[self.profile][key]
        elif self.strict_profile:
            raise Configuration_Exception('no settings value found for: ' + key)
        self.get('quiet', False) or print('[config] Warning: no value found for key: ' + str(key))
        return default


    def __set_profile(self, prf):
        if prf in self.settings:
            self.profile = prf
        else:
            raise Configuration_Exception('no settings dictionary found for profile: ' + prf)

    def __get_profile(self):
        return self.profile

    settings_profile = property(__get_profile, __set_profile)


    ########
    # lang #
    ########

    def get_translation(self, key, **kwargs):
        if key in self.captions[self.lang]:
            return self.captions[self.lang][key].format(**kwargs)
        elif self.lang in self.default_captions and key in self.default_captions[self.lang]:
            return self.default_captions[self.lang][key].format(**kwargs)
        elif self.strict_lang:
            raise Configuration_Exception('no caption found for: ' + key)
        return '?'


    def __set_lang(self, lang):
        if lang in self.captions:
            self.lang = lang
        else:
            raise Configuration_Exception('no captions dictionary found for language: ' + lang)

    def __get_lang(self):
        return self.lang

    language = property(__get_lang, __set_lang)


    ##########
    # keymap #
    ##########

    def get_key(self, key):
        if key in self.maps[self.kmap]:
            return self.maps[self.kmap][key]
        elif self.kmap in self.maps and key in self.default_maps[self.kmap]:
            return self.default_maps[self.kmap][key]
        elif self.strict_keymap:
            raise Configuration_Exception('no key found for: ' + key)
        return []


    def get_valid_keys(self):
        return self.maps[self.kmap].keys()


    def __set_map(self, kmap):
        if kmap in self.maps:
            self.kmap = kmap
        else:
            raise Configuration_Exception('no keymap dictionary found for: ' + kmap)

    def __get_map(self):
        return self.kmap

    keymap = property(__get_map, __set_map)
