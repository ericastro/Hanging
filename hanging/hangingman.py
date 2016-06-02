#/usr/bin/env python
# -*- coding: utf-8 -*-

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

from collections import namedtuple
import inspect
import os
import os.path
import random


class Engine:
    """Define game logic for the normal mode."""

    def __init__(self, word, tries):
        """The game logic for the normal mode.

        :param word: The word to guess.
        :param blanks: The blank underscores that are showed to the player.
        :param guesses: List of the letters tried by the player.
        :param wrong_guesses: List of the wrong guesses made by the player.
        :param tries: The number of tries available.
        """
        self._word = [letter for letter in word]
        self._blanks = [None for _ in range(len(self._word))]
        self._guesses = []
        self._wrong_guesses = []
        self._tries = tries
    
    @property
    def word_letters(self):
        return self._word
    
    @property
    def word(self):
        return ''.join(self.word_letters)
    
    @property
    def blanks(self):
        return self._blanks
    
    @property
    def still_not_correct(self):
        return self.word_letters != self.blanks
    
    @property
    def tries_left(self):
        return self._tries

    @property
    def more_tries(self):
        return self.tries_left > 0
    
    @property
    def guesses(self):
        return self._guesses
    
    @property
    def wrong_guesses(self):
        return self._wrong_guesses
    
    def indexes(self, sequence, element):
        return tuple(index for index, item in enumerate(sequence) if item == element)
     
    def fill_blanks(self, function):
        letter = function()
        inds = self.indexes(self.word, letter)
        if inds:
            for index in inds:
                self.blanks[index] = letter
            self.guesses.append(letter)
            return True
        self.wrong_guesses.append(letter)
        self.tries_left -= 1
        return False


class Interface:
    '''Define the interface for the text mode version of the game.'''
    
    def __init__(self):
        self._level = None
        self._word = None

    def __call__(self, wrongs, guesses, tries, blanks):
        print '\n'
        print 80 * '#'
        print 'Wrong guesses: %s' % self.interface_wrong_guesses(wrongs)
        print 'Guesses: %s' % self.interface_guesses(guesses)
        print 'Chances left: %d' % tries
        print '\n'
        print self.interface_blanks(blanks)

    def interface_guesses(self, guesses):
        return ', '.join(guesses)

    def interface_wrong_guesses(self, wrongs):
        return ', '.join(wrongs)

    def interface_blanks(self, blanks):
        interface_blanks = ['_' if elem == None else elem for elem in blanks]
        return ' '.join(interface_blanks)

    @property
    def level(self):
        return self._level

    @property
    def word(self):
        return self._word

    def choose_level(self, input_func):
        choice = int(input_func())
        Level = namedtuple('Level', 'Name Errors')
        level = {
                1: Level('easy', 7),
                2: Level('medium', 10),
                3: Level('hard', 12)
                }
        self._level = level[choice]
        return self._level

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
                'choose_level': 'Choose a level to play (1-Easy, 2-Medium, 3-Hard): ',
                'fill_blanks': 'Enter a letter: ',
                'play_again': '\nDo you want to play again (yes or no)? ',
                }
        return raw_input(prompts[choice])

    def greeting(self):
        print """
        ************************
        *      HANGINGMAN      *
        ************************
    
        The rules are pretty simple:
    
        Guess the word or the guy gets hanged. Of course, for now there's no guy,
        because the creator of this game haven't made the drawings yet. But you
        get the idea. Use a little imagination, alright?
    
        """

    def congratulations(self):
        print '\n'
        print 'Congratulations, you won!'
        print 'The word is %s.' % self.word.upper()

    def loose(self):
        print '\n'
        print 'Hey, sorry, you lost.'
        print 'Better luck next time!'

    def play_again(self, input_func):
        choice = str(input_func())
        if not choice.startswith('y'): exit(0)


def main():
    interface = Interface()
    interface.greeting()
    while True:
        level = interface.choose_level(interface.prompt)
        word = interface.word_to_guess(level.Name)
        game = Engine(word, level.Errors)
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
