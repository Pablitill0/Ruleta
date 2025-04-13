import random
import time
# Voy a tener que hacer que la funcion recoja y devuelva siempre la informacion de todos los jugadores si quiero que los comodines hagan su funcion
# Aplica el resultado de la ruleta al jugador
def apply_wheel_result(jugador_activo, sector, jugadores_totales):
    if sector == "BANKRUPT":
        jugador_activo["score"] = 0
        print(f"{jugador_activo['name']} cayó en BANCARROTA y perdió todos sus puntos!")
    elif sector == "LOSE_TURN":
        jugador_activo["turn"] = False
        print(f"{jugador_activo['name']} pierde el turno.")
    elif sector == "ME_LO_QUEDO":
        print(f"\n{jugador_activo['name']} cayo en el comodin 'ME LO QUEDO'.")

        # Buscar otros jugadores con puntos > 0 para robarles
        jugadores_con_puntos = []
        for participante in jugadores_totales: # Usamos 'participante' para el bucle
            if participante["name"] != jugador_activo["name"] and participante["score"] > 0:
                jugadores_con_puntos.append({"name": participante["name"], "score": participante["score"]})

        # Si no hay nadie a quien robar
        if not jugadores_con_puntos:
            print("¡Vaya! Nadie mas tiene puntos para que se los quites.")
            return jugador_activo
            

            # Pedir eleccion hasta que sea valida
            while True:
                # Mostrar jugadores a los que se puede robar y sus puntos
                print("Puedes robarle TODOS los puntos a uno de estos jugadores:")
                for opcion_jugador in jugadores_con_puntos: # Usamos 'opcion_jugador'
                    print(f"- {opcion_jugador['name']} ({opcion_jugador['score']} puntos)")

                nombre_jugador_elegido = input(f"\nElige un jugador: ").lower()
                # Evitar elegirse a si mismo
                if nombre_jugador_elegido == jugador_activo["name"].lower():
                    print("No puedes elegirte a ti mismo. Intenta de nuevo.")
                    continue

                # Buscar el diccionario completo del jugador elegido (que debe tener puntos)
                jugador_objetivo = None # Variable en espanol (referencia al diccionario)
                puntos_robados = 0
                for jugador_original in jugadores_totales: # Usamos 'jugador_original' para el bucle
                    # Comparamos con la variable en espanol
                    if jugador_original["name"].lower() == nombre_jugador_elegido and jugador_original["name"] != jugador_activo["name"] and jugador_original["score"] > 0:
                        jugador_objetivo = jugador_original
                        puntos_robados = jugador_objetivo["score"]
                        break # Encontrado

                # Si se encontro un objetivo valido, realizar el robo
                if jugador_objetivo:
                    print(f"\n¡Perfecto! Le quitaras {puntos_robados} puntos a {jugador_objetivo['name']}.")

                    # Transferir puntos y poner a 0 al robado
                    jugador_activo["score"] += puntos_robados
                    jugador_objetivo["score"] = 0

                    print(f"{jugador_objetivo['name']} ahora tiene {jugador_objetivo['score']} puntos.")
                    print(f"Tu nueva puntuacion: {jugador_activo['score']}")
                    break # Salir del bucle while

                else:
                    # Nombre invalido o jugador sin puntos
                    # Usamos la variable en espanol en el mensaje de error
                    print(f"Error: '{nombre_jugador_elegido}' no es un jugador valido al que puedas robar. Revisa la lista e intenta de nuevo.")


    elif sector == "SE_LO_DOY":
        print(f"\n{jugador_activo['name']} cayo en el comodin 'SE LO DOY'.")

        # Comprobar si el jugador actual tiene puntos para dar
        if jugador_activo["score"] <= 0:
            print("No tienes puntos para darle a nadie. ¡Que lastima!")
        else:
            # Buscar a todos los demas jugadores (posibles receptores)
            nombres_otros_jugadores = [] # Variable en espanol
            for participante in jugadores_totales: # Usamos 'participante' para el bucle
                if participante["name"] != jugador_activo["name"]:
                    nombres_otros_jugadores.append(participante["name"])

            # Mostrar a quien se le pueden dar los puntos
            print(f"Puedes darle TODOS tus {jugador_activo['score']} puntos a uno de estos jugadores:")
            for jugador_disponible in nombres_otros_jugadores:
                print(f"- {jugador_disponible}")

            # Pedir eleccion hasta que sea valida
            while True:
                nombre_jugador_elegido = input(f"Elige a quien darle tus puntos: ").lower() # Variable en espanol

                # Evitar elegirse a si mismo
                if nombre_jugador_elegido == jugador_activo["name"].lower():
                    print("No puedes elegirte a ti mismo. Intenta de nuevo.")
                    continue

                # Buscar el diccionario completo del jugador elegido
                jugador_receptor = None # Variable en espanol (referencia al diccionario)
                for jugador_original in jugadores_totales: # Usamos 'jugador_original' para el bucle
                    # Comparamos con la variable en espanol
                    if jugador_original["name"].lower() == nombre_jugador_elegido and jugador_original["name"] != jugador_activo["name"]:
                        jugador_receptor = jugador_original
                        break # Encontrado

                # Si se encontro un receptor valido, realizar la donacion
                if jugador_receptor:
                    puntos_a_dar = jugador_activo["score"]
                    print(f"\n¡Decidido! Le daras tus {puntos_a_dar} puntos a {jugador_receptor['name']}.")

                    # Transferir puntos y poner a 0 al donante
                    jugador_receptor["score"] += puntos_a_dar
                    jugador_activo["score"] = 0

                    print(f"{jugador_receptor['name']} ahora tiene {jugador_receptor['score']} puntos.")
                    print(f"Tu nueva puntuacion: {jugador_activo['score']}")
                    break # Salir del bucle while

                else:
                    # Nombre invalido
                    # Usamos la variable en espanol en el mensaje de error
                    print(f"Error: '{nombre_jugador_elegido}' no es un jugador valido. Revisa la lista e intenta de nuevo.")
    else:
        jugador_activo["score"] += sector
        print(f"{jugador_activo['name']} gana {sector} puntos!")
    return jugador_activo 
    #DEVUELVE los cambios al jugador, y si hay cambios a los demas jugadores mediante jugadores_totales {puede que cambie el nombre}

