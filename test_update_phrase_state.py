import pytest
from game1 import update_phrase_state

def test_update_phrase_state():
    phrase = "hello world"
    phrase_state = "_____ _____"
    guessed_letter = "o"

    result = update_phrase_state(phrase, phrase_state, guessed_letter)

    # Позиции "o" в "hello world": индексы 4 и 7
    # Итоговая строка должна быть: "____o _o___"
    assert result == "____o _o___"
