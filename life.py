#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright (C) 2016  Tom Pickering                                     #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import curses

from os import popen
from time import sleep
from sys import stderr as err

from prebuilts import glider, glider_gun

import locale
locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

# Unicode 'FULL BLOCK'
BLOCK = u'\u2588'
EMPTY = u' '
PAD = {'x': 2, 'y': 1}
LIVE = True
DEAD = False
TIMESTEP = 0.1

# Cell width in characters
CHARS_PER_CELL = 2


class Grid(object):

    def __init__(self, width=20, height=20):
        self.data = [DEAD] * width * height
        self.size = (width, height)
        self.rules = []
        self.updates = []

    def in_bounds(self, idx):
        x, y = idx
        return x >= 0 and x < self.size[0] and y >= 0 and y < self.size[1]

    def __getitem__(self, idx):
        valid = self.in_bounds(idx)
        return valid and self.data[idx[1]*self.size[0] + idx[0]] or False

    def __setitem__(self, idx, val):
        assert self.in_bounds(idx)
        self.data[idx[1]*self.size[0] + idx[0]] = val

    def clear_updates(self):
        self.updates = []

    # Generates positions in grid
    def positions(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                yield (x, y)

    def add_rule(self, cond, val):
        def rule(cond, val):
            def r(n):
                if cond(n):
                    return val
                return None
            return r
        self.rules.append(rule(cond, val))

    # Return the number of live cells surrounding pos
    def neighbours(self, pos):
        x, y = pos
        r = range(-1, 2)
        idxs = [[x + dx, y + dy] for dx in r for dy in r if (dx, dy) != (0, 0)]
        return len([self[p] for p in idxs if self[p] is LIVE])

    # Apply rules to each cell
    def step(self):
        for p in self.positions():
            n = self.neighbours(p)
            for rule in self.rules:
                newval = rule(n)
                if newval in (LIVE, DEAD):
                    if self[p] != newval:
                        self.updates.append({'pos': p, 'val': newval})
                    break  # First rule wins in conflicts
        for upd in self.updates:
            self[upd['pos']] = upd['val']

    # Draw entire grid unconditionally
    def draw_full(self, win):
        s = u''
        i = j = 0
        row_complete = lambda: i == self.size[0] - 1
        for idx in range(len(self.data)):
            i = idx % self.size[0]
            s += self.data[idx] is LIVE and BLOCK or EMPTY
            if row_complete():
                win.addstr(j + PAD['y'], PAD['x'], s.encode('utf-8'))
                s = u''
                j += 1

    # Draw only updates stored on the object
    def draw_updates(self, win):
        for upd in self.updates:
            pos = upd['pos']
            s = self[pos] is LIVE and BLOCK or EMPTY
            str_x = pos[0] * CHARS_PER_CELL + PAD['x']
            str_y = pos[1] + PAD['y']
            win.addstr(str_y, str_x, s.encode('utf-8'))

    def draw(self, win, updates_only=False):
        if updates_only:
            self.draw_updates(win)
            self.clear_updates()
        else:
            self.draw_full(win)
        win.refresh()


def die(msg):
    curses.endwin()
    err.write(msg)
    exit(1)


def main(win):
    curses.curs_set(0)
    h, w = map(int, popen('stty size', 'r').readline().split())

    if CHARS_PER_CELL > 1:
        global BLOCK, EMPTY
        BLOCK *= CHARS_PER_CELL
        EMPTY *= CHARS_PER_CELL
        w /= CHARS_PER_CELL

    grid = Grid(w - 2*PAD['x'], h - 2*PAD['y'])

    # Initial cell configuration
    initial_live = []
    initial_live.extend(glider_gun(1, 1))
    initial_live.extend(glider(1, 20))
    initial_live.extend(glider(8, 21))

    try:
        for p in initial_live:
            grid[p] = LIVE
    except AssertionError:
        die('Terminal size too small for initial cell configuration')

    # Full draw of initial setup
    grid.draw(win)

    # Rule definitions
    grid.add_rule(lambda n: n < 2, DEAD)
    grid.add_rule(lambda n: n > 3, DEAD)
    grid.add_rule(lambda n: n == 3, LIVE)

    while True:
        grid.draw(win, updates_only=True)
        grid.step()
        sleep(TIMESTEP)

if __name__ == '__main__':
    curses.wrapper(main)
