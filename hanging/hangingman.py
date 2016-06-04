#/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################
#
# Copyright (C) 2016 Alexandre Paloschi Horta - http://alexhorta.com
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program (see LICENSE for details).
#     If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################


from engines import Normal, Sniper
from interface import Interface


def pick_engine(_mode, *args):
    if _mode == 1:
        return Normal(*args)
    elif _mode == 2:
        return Sniper(*args)

def main():
    interface = Interface()
    interface.greeting()
    while True:
        mode = interface.choose_mode(interface.prompt)
        level = interface.choose_level(interface.prompt)
        word = interface.word_to_guess(level.Name)
        game = pick_engine(mode, word, level.Errors)
        while game.more_tries and game.still_not_correct:
            data = (
                   game.wrong_guesses,
                   game.guesses,
                   game.tries_left,
                   game.blanks,
               )
            interface(*data)
            game.fill_blanks(interface.prompt)
        else:
            if not game.more_tries:
                interface.loose()
            elif not game.still_not_correct:
                interface.congratulations()
            interface.play_again(interface.prompt)


if __name__ == '__main__':
    main()
