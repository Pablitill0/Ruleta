import pytest
from game1 import check_win_condition  # Замените на правильный модуль

# Пример теста для функции check_win_condition
def test_check_win_condition():
    # Пример строки, где все буквы угаданы
    phrase_state = "A_B_C"
    result = check_win_condition(phrase_state)
    assert result == False  # Строка содержит "_", значит победы нет

    # Пример строки, где все буквы угаданы
    phrase_state = "ABC"
    result = check_win_condition(phrase_state)
    assert result == True  # Строка не содержит "_", значит победа есть

