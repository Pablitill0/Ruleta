import pytest
from unittest.mock import patch

# Пример функции, которую ты хочешь протестировать
def apply_wheel_result(player, sector):
    if sector == "BANKRUPT":
        player["score"] = 0
        print(f"{player['name']} cayó en BANCARROTA y perdió todos sus puntos!")
    elif sector == "LOSE_TURN":
        player["turn"] = False
        print(f"{player['name']} pierde el turno.")
    else:
        player["score"] += sector
        print(f"{player['name']} gana {sector} puntos!")
    return player

# Пример теста для "BANKRUPT"
def test_apply_wheel_result_bankrupt():
    player = {"name": "Jugador1", "score": 100, "turn": True}
    
    with patch("builtins.print") as mock_print:
        result = apply_wheel_result(player, "BANKRUPT")
        
        # Проверяем, что score стал равен 0
        assert result["score"] == 0
        # Проверяем, что turn остался True
        assert result["turn"] == True
        # Проверяем, что правильное сообщение напечатано
        mock_print.assert_called_with("Jugador1 cayó en BANCARROTA y perdió todos sus puntos!")

# Пример теста для "LOSE_TURN"
def test_apply_wheel_result_lose_turn():
    player = {"name": "Jugador1", "score": 100, "turn": True}
    
    with patch("builtins.print") as mock_print:
        result = apply_wheel_result(player, "LOSE_TURN")
        
        # Проверяем, что score не изменился
        assert result["score"] == 100
        # Проверяем, что turn стал False
        assert result["turn"] == False
        # Проверяем, что правильное сообщение напечатано
        mock_print.assert_called_with("Jugador1 pierde el turno.")

# Пример теста для обычного числа (например, 200)
def test_apply_wheel_result_score():
    player = {"name": "Jugador1", "score": 100, "turn": True}
    
    with patch("builtins.print") as mock_print:
        result = apply_wheel_result(player, 200)
        
        # Проверяем, что score увеличился на 200
        assert result["score"] == 300
        # Проверяем, что turn остался True
        assert result["turn"] == True
        # Проверяем, что правильное сообщение напечатано
        mock_print.assert_called_with("Jugador1 gana 200 puntos!")
