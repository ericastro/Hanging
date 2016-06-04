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


from collections import namedtuple
import inspect
import os
import os.path
import random


class Interface:
    '''Define the interface for the text mode version of the game.'''
    
    def __init__(self):
        self._mode = None
        self._level = None
        self._word = None

    def __call__(self, wrongs, guesses, tries, blanks):
        print('\n')
        print(80 * '#')
        print('Wrong guesses: {}'.format(self.interface_wrong_guesses(wrongs)))
        print('Guesses: {}'.format(self.interface_guesses(guesses)))
        print('Chances left: {}'.format(tries))
        print('\n')
        print(self.interface_blanks(blanks))

    def interface_guesses(self, guesses):
        return ', '.join(guesses)

    def interface_wrong_guesses(self, wrongs):
        return ', '.join(wrongs)

    def interface_blanks(self, blanks):
        interface_blanks = ['_' if elem == None else elem for elem in blanks]
        if self._mode == 1:
            return ' '.join(interface_blanks)
        elif self._mode == 2:
            sniper_indexes = [str(index+1) for index in range(len(blanks))]
            sniper_blanks = ' '.join(interface_blanks)
            sniper_indexes = ' '.join(sniper_indexes)
            return sniper_blanks + '\n' + sniper_indexes

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level_choice):
        self._level = level_choice

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, random_word):
        self._word = random_word

    def choose_mode(self, input_func):
        self._mode = int(input_func())
        return self._mode

    def choose_level(self, input_func):
        choice = int(input_func())
        Level = namedtuple('Level', 'Name Errors')
        level = {
                1: Level('easy', 7),
                2: Level('medium', 10),
                3: Level('hard', 12)
                }
        self.level = level[choice]
        return self.level

    def word_to_guess(self, level):
        language = ''.join(('en_us', '_'))
        words = ''.join((language, self.level.Name, '.txt'))
        path = os.path.abspath(os.path.dirname(__file__))
        words_file = os.path.join(path, 'words', words)
        with open(words_file, 'r') as wf:
            self.word = random.choice(wf.readlines()).strip('\n')
            return self.word

    def prompt(self):
        choice = inspect.stack()[1][3]
        prompts = {
                'choose_mode': '\nChoose a game mode to play (1-Normal, 2-Sniper): ',
                'choose_level': '\nChoose a level to play (1-Easy, 2-Medium, 3-Hard): ',
                'fill_blanks': 'Enter a letter: ',
                'play_again': '\nDo you want to play again (yes or no)? ',
                }
        return input(prompts[choice])

    def greeting(self):
        print("""
        ************************
        *      HANGINGMAN      *
        ************************
    
        The rules are pretty simple:
    
        Guess the word or the guy gets hanged. Of course, for now there's no guy,
        because the creator of this game haven't made the drawings yet. But you
        get the idea. Use a little imagination, alright?

        There are two game modes.

        The normal mode is the one everyone knows, you pick a letter and if you
        guessed right, all ocurrences of that letter in the word are uncovered.
        If you guessed wrong, you lose a chance.

        In the sniper mode, you must supply an index and the letter you chose. If
        you guessed right, you win three more chances to guess. If you miss the
        guess you lose one chance. That mode is way, way harder.
    
        """)

    def congratulations(self):
        print('\n')
        print('Congratulations, you won!')
        print('The word is {}.'.format(self.word.upper()))

    def loose(self):
        print('\n')
        print('Hey, sorry, you lost.')
        print('Better luck next time!')

    def play_again(self, input_func):
        choice = str(input_func())
        if not choice.startswith('y'): exit(0)
