kanjitest
=========

(name subject to change)

A little command line tool to help you learn your kanji. It works like flip cards - there's no actual user input like drawing a sign. It's probably far from being finished and has a few deficits in its current design but it works. It was created in a rush to prevent me from drowning in physical flip cards and since it does exactly what I need (for now), further improvements are unlikely (for now).

Currently there's only a text-based user interface.


How it works
------------

Kanji are read from a database (see **Setup**) and filtered depending on your configuration and arguments. Whatever survived your filters is sequentially printed in a text area in random order.

Only previously configured fields are visible, a subsequent (configurable) keypress reveals the whole dataset. You can change the priority of the currently displayed kanji.


Setup
-----

There's no installation procedure (currently). Create an alias or whatever suits your needs, e.g.:

    alias kanjitest='python3 <path to kanjitest folder>/main.py'

You have to supply the script a sqlite3 database. The data of each kanji is stored in a single dictionary, associated with a textbook, an id (referring to the textbook), a priority and altogether saved as one row. There are very rudimental scripts for the table structure, creating and inserting values in `helpers`.


Requirements
------------

- Python >3.3 (3.0 < x < 3.3 is untested)
- [Urwid](https://pypi.python.org/pypi/urwid/)
- A terminal emulator with proper uft8 support as well as a decent font and anti-aliasing
