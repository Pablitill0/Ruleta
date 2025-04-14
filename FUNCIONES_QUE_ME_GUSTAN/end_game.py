import random
import time

# Función para terminar el juego — actualizada
def end_game(players):
    print("\n¡Juego terminado! Resultados finales:")

    # Ordena la lista original de jugadores por puntaje en orden descendente
    players.sort(key=lambda p: p["score"], reverse=True)
    

    # Imprime los resultados de cada jugador
    for player in players:
        print(f"{player['name']} - {player['score']} puntos")

    # Muestra al ganador (jugador con mayor puntaje)
    winner = players[0]
    print(f"\n¡El ganador es {winner['name']} con {winner['score']} puntos!")