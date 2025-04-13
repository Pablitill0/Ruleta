import pytest
import random
from unittest.mock import patch

# Оригинальная функция
def select_phrase(phrases):
    return random.choice(phrases)

# Тест: выбор фразы из списка
def test_select_phrase():
    phrases = ["фраза 1", "фраза 2", "фраза 3"]
    
    with patch("random.choice", return_value="фраза 2"):
        assert select_phrase(phrases) == "фраза 2"  # Мокируем на возврат "фраза 2"

# Тест: пустой список
def test_select_phrase_empty():
    with patch("random.choice", return_value=None):
        assert select_phrase([]) is None  # Для пустого списка возвращаем None

# Тест: один элемент в списке
def test_select_phrase_single_item():
    with patch("random.choice", return_value="единственная фраза"):
        assert select_phrase(["единственная фраза"]) == "единственная фраза"
