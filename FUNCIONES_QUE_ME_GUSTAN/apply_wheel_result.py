import random
import time
# Voy a tener que hacer que la funcion recoja y devuelva siempre la informacion de todos los jugadores si quiero que los comodines hagan su funcion
# Aplica el resultado de la ruleta al jugador
def apply_wheel_result(player, sector, players):
    if sector == "BANKRUPT":
        player["score"] = 0
        print(f"{player['name']} cayó en BANCARROTA y perdió todos sus puntos!")
    elif sector == "LOSE_TURN":
        player["turn"] = False
        print(f"{player['name']} pierde el turno.")
    elif sector == "ME_LO_QUEDO":  #ESTA OPCION NO ESTA DISPONIBLE EN EL MODO DE UN SOLO JUGADOR
        nombres_jugadores = []
        puntos_jugadores = []
        for jugador in players:
            nombre = jugador["name"]
            puntos = jugador["score"]
            nombres_jugadores.append(nombre)
            puntos_jugadores.append(puntos)
        while True:
            jugador_elegido = input(f"{player['name']} cayó en el comodin 'me lo quedo'\nElige un jugador con el que utilizarlo: ")
            player["score"] += 

    elif sector == "SE_LO_DOY": #ESTA OPCION NO ESTA DISPONIBLE EN EL MODO DE UN SOLO JUGADOR
        jugador_elegido = input(f"{player['name']} cayó en el comodin 'se lo doy'\nElige un jugador con el que utilizarlo: ")
        nombres_jugadores = []
        puntos_jugadores = []
        for jugador in players:
            nombre = jugador["name"]
            puntos = jugador["score"]
            nombres_jugadores.append(nombre)
            puntos_jugadores.append(puntos)
        while True:
            jugador_elegido = input(f"{player['name']} cayó en el comodin 'me lo quedo'\nElige un jugador con el que utilizarlo: ")
            player["score"] += 
    else:
        player["score"] += sector
        print(f"{player['name']} gana {sector} puntos!")
    return player 
    #DEVUELVE los cambios al jugador, y si hay cambios a los demas jugadores mediante PLAYERS {puede que cambie el nombre}

