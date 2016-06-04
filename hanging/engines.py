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


class Normal:
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
        self.wrong_guesses.append(letter)
        self._tries -= 1


class Sniper(Normal):
    '''Define game logic for the sniper mode.'''

    def __init__(self, *args):
        super(Sniper, self).__init__(*args)

    def fill_blanks(self, function):
        index, letter = function().split()
        index = int(index) - 1
        if self.word_letters[index] == letter:
            self.blanks[index] = letter
            self.guesses.append(letter)
            self._tries += 3
        else:
            self.wrong_guesses.append(letter)
            self._tries -= 1
