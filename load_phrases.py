import random
import time

# Función para cargar frases desde archivos según la dificultad
def load_phrases(difficulty):
    # Abrimos el archivo correspondiente según la dificultad
    if difficulty == "facil":
        file_name = "facil.txt"
    elif difficulty == "medio":
        file_name = "medio.txt"
    else:  # dificultad difícil
        file_name = "dificil.txt"
    
    try:
        # Leemos el archivo y devolvemos la lista de frases
        with open(file_name, "r", encoding="utf-8") as file:
            phrases = [line.strip() for line in file.readlines()]
        return phrases
    except FileNotFoundError:
        print(f"Error: El archivo {file_name} no se encuentra.")
        return []