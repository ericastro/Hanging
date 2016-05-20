import inspect
import os
import os.path
import random
from collections import namedtuple


class Engine:

    def __init__(self, word, tries):
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
    def interface_blanks(self):
        interface_blanks = ['_' if elem == None else elem for elem in self.blanks]
        return ' '.join(interface_blanks)
    
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
    def interface_guesses(self):
        return ', '.join(self.guesses)
    
    @property
    def wrong_guesses(self):
        return self._wrong_guesses

    @property
    def interface_wrong_guesses(self):
        return ', '.join(self.wrong_guesses)

    @property
    def interface(self):
        print '\n'
        print 80 * '#'
        print 'Wrong guesses: %s' % self.interface_wrong_guesses
        print 'Guesses: %s' % self.interface_guesses
        print 'Chances left: %d' % self.tries_left
        print '\n'
        print self.interface_blanks
    
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
 

def choose_level(input_func):
    choice = int(input_func())
    Level = namedtuple('Level', 'Name Errors')
    level = {
            1: Level('easy', 7),
            2: Level('medium', 10),
            3: Level('hard', 12)
            }
    return level[choice]

def word_to_guess(level):
    words = ''.join(('en_us_', level.Name, '.txt'))
    path = os.path.abspath(os.path.dirname(__file__))
    words_file = os.path.join(path, 'words', words)
    with open(words_file, 'r') as wf:
        return random.choice(wf.readlines()).strip('\n')

def prompt():
    choice = inspect.stack()[1][3]
    prompts = {
            'choose_level': 'Choose a level to play (1-Easy, 2-Medium, 3-Hard): ',
            'fill_blanks': 'Enter a letter: ',
            'play_again': '\nDo you want to play again (yes or no)? ',
            }
    return raw_input(prompts[choice])

def greeting():
    print """
    ************************
    *      HANGINGMAN      *
    ************************

    The rules are pretty simple:

    Guess the word or the guy gets hanged. Of course, for now there's no guy,
    because the creator of this game haven't made the drawings yet. But you
    get the idea. Use a little imagination, alright?

    """

def main():
    greeting()
    while True:
        level = choose_level(prompt)
        word = word_to_guess(level)
        game = Engine(word, level.Errors)
        while game.more_tries and game.still_not_correct:
            game.interface
            game.fill_blanks(prompt)
        else:
            if not game.more_tries:
                pass
            elif not game.still_not_correct:
                pass


if __name__ == '__main__':
    main()
