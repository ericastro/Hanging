from collections import namedtuple

import pytest

import hangingman
from hangingman import prompt


def test_choose_level(monkeypatch):
    Level = namedtuple('Level', 'Name Errors')
    with monkeypatch.setattr(__builtins__, 'raw_input', lambda: '1'):
        assert(hangingman.choose_level(prompt) == ('easy', 7))

def test_choose_level_string():
    with pytest.raises(KeyError):
        hangingman.choose_level(prompt)
