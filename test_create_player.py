import pytest
from game1 import create_player  # Убедись, что импортируешь правильный модуль

# Тест: создание игрока
def test_create_player():
    result = create_player("John")  # Создаем игрока с именем "John"
    
    # Проверяем, что словарь имеет правильные значения
    assert result == {"name": "John", "score": 0, "turn": False}
