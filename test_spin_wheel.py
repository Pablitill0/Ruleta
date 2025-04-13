import pytest
import random
from game1 import spin_wheel  # Убедись, что импортируешь правильный модуль

# Тест: вращение рулетки и проверка значений
def test_spin_wheel():
    # Используем MonkeyPatch для замены random.choice
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(random, "choice", lambda x: 100)  # Мокируем random.choice, чтобы вернуть 100
        result = spin_wheel()  # Вращаем рулетку (мы замокировали random.choice)
        assert result == 100  # Проверяем, что вернулось значение 100

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(random, "choice", lambda x: "BANKRUPT")
        result = spin_wheel()
        assert result == "BANKRUPT"  # Проверяем, что вернулось значение "BANKRUPT"
