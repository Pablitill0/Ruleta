from unittest.mock import mock_open, patch

# Оригинальная функция с открытием файлов
def load_phrases(difficulty):
    if difficulty == "facil":
        file_name = "facil.txt"
    elif difficulty == "medio":
        file_name = "medio.txt"
    else:  # dificultad difícil
        file_name = "dificil.txt"
    
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            phrases = [line.strip() for line in file.readlines()]
        return phrases
    except FileNotFoundError:
        print(f"Error: El archivo {file_name} no se encuentra.")
        return []


# --- Тест для "facil" ---
mock_data_facil = "frase 1\nfrase 2\n"
with patch("builtins.open", mock_open(read_data=mock_data_facil)) as mock_file:
    result = load_phrases("facil")
    mock_file.assert_called_once_with("facil.txt", "r", encoding="utf-8")
    print("✅ Test 'facil' пройден, файл открыт корректно")
    print(result)  # Добавляем вывод для проверки результата

# --- Тест для "medio" ---
mock_data_medio = "medio frase 1\nmedio frase 2\n"
with patch("builtins.open", mock_open(read_data=mock_data_medio)) as mock_file:
    result = load_phrases("medio")
    mock_file.assert_called_once_with("medio.txt", "r", encoding="utf-8")
    print("✅ Test 'medio' пройден, файл открыт корректно")
    print(result)  # Добавляем вывод для проверки результата

# --- Тест для "dificil" ---
mock_data_dificil = "difícil 1\nmás difícil\n"
with patch("builtins.open", mock_open(read_data=mock_data_dificil)) as mock_file:
    result = load_phrases("dificil")
    mock_file.assert_called_once_with("dificil.txt", "r", encoding="utf-8")
    print("✅ Test 'dificil' пройден, файл открыт корректно")
    print(result)  # Добавляем вывод для проверки результата
