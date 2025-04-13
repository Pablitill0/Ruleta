import random
import time

# El ciclo principal del juego
def main():
    # Solicita el número de jugadores
    num_players = int(input('Introduce el numero de jugadores: '))
    # Solicita la dificultad del juego
    difficulty = input("Elige la dificultad (facil, medio, dificil): ").strip().lower()

    # Inicializa el juego y obtiene los jugadores y la frase
    phrases = load_phrases(difficulty)
    if not phrases:  # Si no hay frases disponibles (archivo no encontrado)
        print("No hay frases disponibles. El juego no puede continuar.")
        return

    players = []
    for i in range(num_players):
        name = input(f'Introduce el nombre del jugador {i + 1}: ')
        player = create_player(name)
        players.append(player)

    # Selecciona una frase aleatoria
    phrase = select_phrase(phrases)
    # Procesa la frase (la convierte en minúsculas)
    phrase = process_phrase(phrase)
    print(f"Frase seleccionada para adivinar: {phrase}")
    
    # Inicializa el estado de la frase (todos los caracteres son guiones bajos)
    phrase_state = "_" * len(phrase) 
    phrase_state = update_phrase_state(phrase, phrase_state, " ")  # Los espacios deben estar visibles desde el inicio
    guessed_letters = set()  # Almacena las letras adivinadas

    # Empieza el juego con un jugador aleatorio
    current_player = random.choice(players)
    current_player["turn"] = True

    # Mientras no se haya adivinado la frase, continúa el juego
    while not check_win_condition(phrase_state):
        for player in players:
            if player["turn"]:
                phrase_state = play_turn(player, phrase, phrase_state, guessed_letters)
                if check_win_condition(phrase_state):
                    break
                # Cambia de turno
                player["turn"] = False
                next_player = players[(players.index(player) + 1) % len(players)]
                next_player["turn"] = True
                time.sleep(1)

    # Termina el juego
    end_game(players)

if __name__ == "__main__":
    main()