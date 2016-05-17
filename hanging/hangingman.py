import inspect
import os
import os.path
import random
from collections import namedtuple
from itertools import count


myself = lambda: inspect.stack()[1][3]


def prompt(name):
    prompts = {
            'choose_level': 'Choose a level to play (1-Easy, 2-Medium, 3-Hard): ',
            'play_again': '\nDo you want to play again (yes or no)? '
            }
    return raw_input(prompts[name])

def choose_level(input_func):
    choice = int(input_func(myself()))
    Level = namedtuple('Level', 'Name Errors')
    level = {
            1: Level('easy', 7),
            2: Level('medium', 10),
            3: Level('hard', 12)
            }
    return level[choice]

def word_to_guess(level):
    words = ''.join(('en_us_', level, '.txt'))
    path = os.path.abspath(os.path.dirname(__file__))
    words_file = os.path.join(path, 'words', words)
    with open(words_file, 'r') as wf:
        return random.choice(wf.readlines()).strip('\n')

def blanks(word, guesses):
    blank_ = list('_' for i in word)
    for i, w in enumerate(word):
        for g in guesses:
            if w == g:
                blank_[i] = g
    blank = ' '.join(blank_)
    check = ''.join(blank_)
    return blank, check

def is_correct(word, blank):
    blank = ''.join(blank)
    return word == blank

def play_again(input_func):
    play = input_func(myself())
    return play.startswith('y')

def main():
    while True:
        guesses = ''
        wrong_guesses = ''
        print '\nHANGINGMAN\n'
        level, limit = choose_level(prompt)
        chances = limit - len(wrong_guesses)
        word = word_to_guess(level)
        blank, check = blanks(word, guesses)
        while True:
            print '\n'
            print '#' * 60
            print 'Your guesses: %s' % guesses
            print 'Wrong guesses: %s' % wrong_guesses
            print 'Chances left: %d' % chances
            print '#' * 60
            print '\n', blank
            guess = raw_input('Enter a letter: ')
            guess = guess.lower()
            guesses += guess
            if guess not in word:
                wrong_guesses = guess
            else:
                pass
            blank, check = blanks(word, guesses)
            chances = limit - len(wrong_guesses)
            if is_correct(word, check):
                print 'You won! The word is %s. Cheers!' % word.upper()
                break
            elif len(wrong_guesses) > limit:
                print 'Too bad, you lost. Maybe another time...'
                break
        if play_again(prompt):
            guesses = ''
            wrong_guesses = ''
        else:
            quit()

if __name__ == '__main__':
    main()
