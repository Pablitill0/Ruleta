import pytest
from game1 import process_phrase  # Убедись, что импортируешь правильный модуль

# Тест: удаление пробелов и приведение к нижнему регистру
def test_process_phrase_basic():
    result = process_phrase("  Hola Mundo  ")
    assert result == "hola mundo"  # Ожидаем "hola mundo" после обработки

# Тест: строка с заглавными буквами
def test_process_phrase_uppercase():
    result = process_phrase("   FRASE EN MAYÚSCULAS   ")
    assert result == "frase en mayúsculas"  # Ожидаем нижний регистр и удаление пробелов

# Тест: уже нормализованная строка
def test_process_phrase_no_change():
    result = process_phrase("sin cambios")
    assert result == "sin cambios"  # Ожидаем, что строка не изменится, так как она уже правильная
