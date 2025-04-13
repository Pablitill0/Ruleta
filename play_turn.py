import random
import time

#Hay que separar esta funcion en 2 pequenas
# El ciclo de juego por turno
def play_turn(player, phrase, phrase_state, guessed_letters):
    print(f"\nTurno de {player['name']}")

    # Gira la ruleta
    sector = spin_wheel()
    print(f"La ruleta cayó en: {sector}")
    
    # Aplica el resultado de la ruleta
    player = apply_wheel_result(player, sector)

    if sector == "LOSE_TURN" or sector == "BANKRUPT":
        return phrase_state
"""
    # El jugador introduce una letra
    guessed_letter = input("Introduce una letra: ").strip().lower()

    # Verifica si la letra ya fue adivinada
    if guessed_letter in guessed_letters:
        print(f"Ya has adivinado la letra '{guessed_letter}'. Intenta con otra.")
        return phrase_state

    guessed_letters.add(guessed_letter)  # Agrega la letra a las letras adivinadas

    # Si la letra está en la frase, actualiza la frase
    if guessed_letter in phrase:
        phrase_state = update_phrase_state(phrase, phrase_state, guessed_letter)
        print(f"¡Bien! La frase ahora es: {phrase_state}")
    else:
        print("Letra incorrecta.")
    
    return phrase_state

"""