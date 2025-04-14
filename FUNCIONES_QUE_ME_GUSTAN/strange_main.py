import random
import time
import string
import os # Necesario para manejar archivos y carpetas

# --- CONSTANTES Y DATOS DEL JUEGO ---

# Nombres de archivos
ARCHIVO_FRASES_FACIL = "frases_facil.txt"
ARCHIVO_FRASES_MEDIO = "frases_medio.txt"
ARCHIVO_FRASES_DIFICIL = "frases_dificil.txt"
ARCHIVO_CLASIFICACION = "clasificacion.txt"

# Ruleta Multijugador (con comodines)
SECTORES_RULETA_MULTI = [75, 50, 100, 150, "PIERDE TURNO", "QUIEBRA", 25, "SE LO DOY", "ME LO QUEDO", 200]
PESOS_RULETA_MULTI    = [4,  4,  2,   2,   2,            2,       1,   1,          1,           1]

# Ruleta Individual (sin comodines ME LO QUEDO/SE LO DOY)
# Reemplazamos comodines con valores (ej. 50 extra y 25 extra) o mas PIERDE TURNO/QUIEBRA
# Opcion simple: quitar comodines y ajustar pesos (total debe sumar)
SECTORES_RULETA_IND = [75, 50, 100, 150, "PIERDE TURNO", "QUIEBRA", 25, 200] # Quitamos SE LO DOY, ME LO QUEDO
# Ajustamos pesos (originales: 4, 4, 2, 2, 2, 2, 1, 1) -> Suma 18. Redistribuimos los 2 puntos faltantes
PESOS_RULETA_IND    = [4,  5,  2,   2,   3,            2,       1,   1] # Suma 20 (ej: +1 a 50, +1 a PIERDE TURNO)


VOCALES = "aeiou"
CONSONANTES = "bcdfghjklmnpqrstvwxyz"
COSTO_VOCAL = 50
MAX_CLASIFICACION = 10 # Maximo numero de entradas en la clasificacion

# --- FUNCIONES DE MANEJO DE ARCHIVOS ---

def generar_archivos_frases_si_no_existen():
    """Crea archivos de frases de ejemplo si no existen."""
    archivos_frases = {
        ARCHIVO_FRASES_FACIL: ["HOLA MUNDO", "CASA GRANDE", "PERRO Y GATO"],
        ARCHIVO_FRASES_MEDIO: ["RUEDA DE LA FORTUNA", "PROGRAMACION EN PYTHON", "ADIVINA LA FRASE"],
        ARCHIVO_FRASES_DIFICIL: ["INTELIGENCIA ARTIFICIAL GENERATIVA", "ALGORITMOS DE ORDENACION", "PARADIGMAS DE PROGRAMACION"]
    }
    for nombre_archivo, frases_ejemplo in archivos_frases.items():
        if not os.path.exists(nombre_archivo):
            print(f"Creando archivo de frases de ejemplo: {nombre_archivo}")
            try:
                with open(nombre_archivo, "w", encoding="utf-8") as f:
                    for frase in frases_ejemplo:
                        f.write(frase + "\n")
            except IOError as e:
                print(f"Error al crear el archivo {nombre_archivo}: {e}")

def cargar_frases(nombre_archivo):
    """Carga frases desde un archivo de texto."""
    frases = []
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                frase = linea.strip().upper() # Limpiar y convertir a mayusculas
                if frase: # Ignorar lineas vacias
                    frases.append(frase)
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo de frases '{nombre_archivo}'.")
        # Podria devolver una lista vacia o salir, aqui devolvemos vacia
    except IOError as e:
        print(f"Error al leer el archivo {nombre_archivo}: {e}")
    return frases

def cargar_clasificacion():
    """Carga la clasificacion desde el archivo."""
    clasificacion = []
    try:
        with open(ARCHIVO_CLASIFICACION, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(":")
                if len(partes) == 2:
                    nombre = partes[0]
                    try:
                        puntos = int(partes[1])
                        clasificacion.append({"nombre": nombre, "puntos": puntos})
                    except ValueError:
                        print(f"Advertencia: Ignorando linea mal formada en clasificacion: {linea.strip()}")
    except FileNotFoundError:
        print("No se encontro archivo de clasificacion. Se creara uno nuevo.")
    except IOError as e:
        print(f"Error al leer la clasificacion: {e}")
    # Ordenar por puntos descendente al cargar
    clasificacion.sort(key=lambda item: item["puntos"], reverse=True)
    return clasificacion

def guardar_clasificacion(clasificacion):
    """Guarda la clasificacion actualizada en el archivo."""
    # Ordenar por puntos y limitar tamaño antes de guardar
    clasificacion.sort(key=lambda item: item["puntos"], reverse=True)
    clasificacion_a_guardar = clasificacion[:MAX_CLASIFICACION] # Tomar solo los mejores N

    try:
        with open(ARCHIVO_CLASIFICACION, "w", encoding="utf-8") as f:
            for entrada in clasificacion_a_guardar:
                f.write(f"{entrada['nombre']}:{entrada['puntos']}\n")
    except IOError as e:
        print(f"Error al guardar la clasificacion: {e}")

def actualizar_clasificacion(jugadores_partida):
    """Anade los resultados de la partida a la clasificacion general."""
    clasificacion_actual = cargar_clasificacion()
    nombres_en_clasificacion = [entrada["nombre"] for entrada in clasificacion_actual]

    for jugador in jugadores_partida:
        nombre_jugador = jugador["nombre"]
        puntos_jugador = jugador["puntos"]

        # Si el jugador ya esta, actualizar si mejora puntos
        actualizado = False
        for i in range(len(clasificacion_actual)):
            if clasificacion_actual[i]["nombre"] == nombre_jugador:
                if puntos_jugador > clasificacion_actual[i]["puntos"]:
                    print(f"¡Nuevo record para {nombre_jugador}!")
                    clasificacion_actual[i]["puntos"] = puntos_jugador
                actualizado = True
                break

        # Si no estaba, anadirlo
        if not actualizado:
            clasificacion_actual.append({"nombre": nombre_jugador, "puntos": puntos_jugador})

    guardar_clasificacion(clasificacion_actual)


# --- FUNCIONES BASICAS DEL JUEGO (TRADUCIDAS) ---

def crear_jugador(nombre):
    # Las claves del diccionario tambien en espanol
    return {"nombre": nombre, "puntos": 0}

def girar_ruleta(es_individual):
    """Simula giro de ruleta segun modo de juego."""
    if es_individual:
        sectores = SECTORES_RULETA_IND
        pesos = PESOS_RULETA_IND
    else:
        sectores = SECTORES_RULETA_MULTI
        pesos = PESOS_RULETA_MULTI

    resultado = random.choices(sectores, weights=pesos, k=1)[0]
    return resultado

def inicializar_estado_frase(frase):
    estado = ""
    for caracter in frase:
        # Usamos isalpha() que funciona con caracteres Unicode (incluye ñ)
        if caracter.isalpha():
            estado += "_"
        else:
            estado += caracter
    return estado

def contar_aciertos(frase, letra):
    return frase.lower().count(letra.lower())

def actualizar_estado_frase(frase_original, estado_actual_frase, letra_adivinada):
    nuevo_estado_lista = list(estado_actual_frase)
    letra_adivinada = letra_adivinada.lower()
    frase_original_lower = frase_original.lower()

    for i in range(len(frase_original_lower)):
        if frase_original_lower[i] == letra_adivinada:
            # Revelar la letra original (mantiene mayus/minus)
            if frase_original[i].isalpha():
                 nuevo_estado_lista[i] = frase_original[i]

    return "".join(nuevo_estado_lista)

def verificar_victoria(estado_frase):
    return "_" not in estado_frase

# --- FUNCIONES DE LOGICA DE TURNO (TRADUCIDAS) ---

def aplicar_resultado_ruleta(jugador_activo, sector, todos_jugadores):
    """Aplica efecto de la ruleta. Devuelve int, "TURNO_TERMINADO" o "COMODIN_TERMINADO"."""
    print(f"La ruleta cayo en: {sector}")
    time.sleep(1)

    if isinstance(sector, int): # Puntos
        print(f"{jugador_activo['nombre']} tiene la oportunidad de ganar {sector} puntos por consonante.")
        return sector

    elif sector == "QUIEBRA":
        jugador_activo["puntos"] = 0
        print(f"¡{jugador_activo['nombre']} cayo en QUIEBRA y perdio todos sus puntos!")
        return "TURNO_TERMINADO"
    elif sector == "PIERDE TURNO":
        print(f"{jugador_activo['nombre']} pierde el turno.")
        return "TURNO_TERMINADO"

    # --- Comodines (logica similar, variables traducidas) ---
    elif sector == "ME LO QUEDO":
        print(f"\n{jugador_activo['nombre']} cayo en el comodin 'ME LO QUEDO'.")
        jugadores_con_puntos = []
        for participante in todos_jugadores:
            # Usamos claves en espanol
            if participante["nombre"] != jugador_activo["nombre"] and participante["puntos"] > 0:
                jugadores_con_puntos.append({"nombre": participante["nombre"], "puntos": participante["puntos"]})

        if not jugadores_con_puntos:
            print("¡Vaya! Nadie mas tiene puntos para que se los quites.")
            return "COMODIN_TERMINADO"

        while True:
            print("\nCandidatos para robar:")
            for opcion_jugador in jugadores_con_puntos:
                print(f"- {opcion_jugador['nombre']} ({opcion_jugador['puntos']} puntos)")
            nombre_elegido = input(f"Elige un jugador: ").lower()

            if nombre_elegido == jugador_activo["nombre"].lower():
                print("No puedes elegirte a ti mismo. Intenta de nuevo.")
                continue

            jugador_objetivo = None
            puntos_robados = 0
            encontrado_valido = False
            for candidato in jugadores_con_puntos:
                if candidato["nombre"].lower() == nombre_elegido:
                    encontrado_valido = True
                    for j_orig in todos_jugadores:
                        if j_orig["nombre"] == candidato["nombre"]:
                            jugador_objetivo = j_orig
                            puntos_robados = jugador_objetivo["puntos"]
                            break
                    break

            if encontrado_valido and jugador_objetivo:
                print(f"\n¡Perfecto! Le quitaras {puntos_robados} puntos a {jugador_objetivo['nombre']}.")
                jugador_activo["puntos"] += puntos_robados
                jugador_objetivo["puntos"] = 0
                print(f"{jugador_objetivo['nombre']} ahora tiene {jugador_objetivo['puntos']} puntos.")
                print(f"Tu nueva puntuacion: {jugador_activo['puntos']}")
                return "COMODIN_TERMINADO"
            else:
                print(f"Error: '{nombre_elegido}' no es un candidato valido. Revisa la lista e intenta de nuevo.")

    elif sector == "SE LO DOY":
        print(f"\n{jugador_activo['nombre']} cayo en el comodin 'SE LO DOY'.")
        if jugador_activo["puntos"] <= 0:
            print("No tienes puntos para darle a nadie. ¡Que lastima!")
            return "COMODIN_TERMINADO"

        nombres_otros = []
        for participante in todos_jugadores:
            if participante["nombre"] != jugador_activo["nombre"]:
                nombres_otros.append(participante["nombre"])

        if not nombres_otros:
             print("No hay otros jugadores a quienes darles tus puntos.")
             return "COMODIN_TERMINADO"

        puntos_a_dar = jugador_activo["puntos"]
        while True:
            print(f"\nCandidatos para recibir tus {puntos_a_dar} puntos:")
            for nombre_disp in nombres_otros:
                print(f"- {nombre_disp}")
            nombre_elegido = input(f"Elige a quien darle tus puntos: ").lower()

            if nombre_elegido == jugador_activo["nombre"].lower():
                print("No puedes elegirte a ti mismo. Intenta de nuevo.")
                continue

            jugador_receptor = None
            encontrado_valido = False
            if nombre_elegido in [n.lower() for n in nombres_otros]:
                 encontrado_valido = True
                 for j_orig in todos_jugadores:
                     if j_orig["nombre"].lower() == nombre_elegido:
                         jugador_receptor = j_orig
                         break

            if encontrado_valido and jugador_receptor:
                print(f"\n¡Decidido! Le daras tus {puntos_a_dar} puntos a {jugador_receptor['nombre']}.")
                jugador_receptor["puntos"] += puntos_a_dar
                jugador_activo["puntos"] = 0
                print(f"{jugador_receptor['nombre']} ahora tiene {jugador_receptor['puntos']} puntos.")
                print(f"Tu nueva puntuacion: {jugador_activo['puntos']}")
                return "COMODIN_TERMINADO"
            else:
                print(f"Error: '{nombre_elegido}' no es un candidato valido. Revisa la lista e intenta de nuevo.")

    return "TURNO_TERMINADO" # Por si acaso

def mostrar_estado_juego(jugador, estado_frase, letras_usadas):
    print("\n" + "="*40)
    print(f"Turno de: {jugador['nombre']} (Puntos: {jugador['puntos']})")
    print(f"Frase: {estado_frase}")
    usadas_voc = sorted([l for l in letras_usadas if l in VOCALES])
    usadas_con = sorted([l for l in letras_usadas if l not in VOCALES])
    print(f"Vocales usadas: {' '.join(usadas_voc)}")
    print(f"Consonantes usadas: {' '.join(usadas_con)}")
    print("="*40)

def obtener_opcion_principal(jugador):
    while True:
        print("\nElige una opcion:")
        print(f"1. Comprar vocal ({COSTO_VOCAL} puntos)")
        print("2. Intentar resolver la frase")
        print("3. Girar la ruleta")
        opcion = input("Tu eleccion (1, 2, 3): ")
        if opcion in ["1", "2", "3"]:
            if opcion == "1" and jugador["puntos"] < COSTO_VOCAL:
                print(f"No tienes suficientes puntos ({jugador['puntos']}) para comprar una vocal.")
                continue
            return int(opcion)
        else:
            print("Opcion invalida. Introduce 1, 2 o 3.")

def comprar_vocal(jugador, frase, estado_frase, letras_usadas):
    if jugador["puntos"] < COSTO_VOCAL:
        print("Error interno: No deberias poder elegir esta opcion sin puntos.")
        return estado_frase, False

    while True:
        vocal = input("Introduce la vocal que quieres comprar: ").lower()
        if len(vocal) != 1 or vocal not in VOCALES:
            print("Entrada invalida. Introduce una unica vocal (a, e, i, o, u).")
            continue
        if vocal in letras_usadas:
            print(f"La vocal '{vocal}' ya ha sido usada. Elige otra.")
            continue

        jugador["puntos"] -= COSTO_VOCAL
        letras_usadas.add(vocal)
        print(f"Has comprado la vocal '{vocal}' por {COSTO_VOCAL} puntos.")
        print(f"Tu puntuacion ahora es: {jugador['puntos']}")

        if vocal in frase.lower():
            print(f"¡Bien! La vocal '{vocal}' esta en la frase.")
            nuevo_estado = actualizar_estado_frase(frase, estado_frase, vocal)
            print(f"Frase actualizada: {nuevo_estado}")
            return nuevo_estado, True
        else:
            print(f"Lo siento, la vocal '{vocal}' no esta en la frase.")
            return estado_frase, True # Accion valida, aunque no acierte

def pedir_consonante(jugador, frase, estado_frase, letras_usadas, valor_ruleta):
    while True:
        consonante = input("Introduce una consonante: ").lower()
        if len(consonante) != 1 or consonante not in CONSONANTES:
            print("Entrada invalida. Introduce una unica consonante.")
            continue
        if consonante in letras_usadas:
            print(f"La consonante '{consonante}' ya ha sido usada. Pierdes el turno.")
            return estado_frase, False # Falla, pierde turno

        letras_usadas.add(consonante)
        if consonante in frase.lower():
            num_aciertos = contar_aciertos(frase, consonante)
            puntos_ganados = valor_ruleta * num_aciertos
            jugador["puntos"] += puntos_ganados
            print(f"¡Correcto! '{consonante}' aparece {num_aciertos} veces.")
            print(f"Ganas {puntos_ganados} puntos ({valor_ruleta} x {num_aciertos}).")
            print(f"Tu puntuacion ahora es: {jugador['puntos']}")
            nuevo_estado = actualizar_estado_frase(frase, estado_frase, consonante)
            print(f"Frase actualizada: {nuevo_estado}")
            return nuevo_estado, True # Exito
        else:
            print(f"Lo siento, la consonante '{consonante}' no esta en la frase. Pierdes el turno.")
            return estado_frase, False # Falla, pierde turno

def intentar_resolver(jugador, frase_real, estado_actual_frase):
    print("\n--- Intentar Resolver ---")
    print(f"Frase actual: {estado_actual_frase}")
    intento = input("Escribe la frase completa que crees que es: ").strip().upper() # Comparar en mayusculas

    if intento == frase_real: # frase_real ya esta en mayusculas
        print(f"¡¡¡CORRECTO!!! ¡Has resuelto la frase!")
        return True # Juego terminado
    else:
        print("Lo siento, esa no es la frase correcta. Pierdes el turno.")
        return False # Juego continua, turno acaba

def finalizar_partida(jugadores):
    print("\n¡Partida terminada! Resultados finales:")
    jugadores.sort(key=lambda j: j["puntos"], reverse=True)

    for jugador in jugadores:
        print(f"- {jugador['nombre']}: {jugador['puntos']} puntos")

    # Actualizar clasificacion general
    print("\nActualizando clasificacion general...")
    actualizar_clasificacion(jugadores)

    # Mostrar ganador(es) de la partida
    if jugadores:
        ganador = jugadores[0]
        ganadores = [j for j in jugadores if j['puntos'] == ganador['puntos']]
        if len(ganadores) > 1:
            nombres_ganadores = ", ".join([g['nombre'] for g in ganadores])
            print(f"\n¡Hay un empate en esta partida entre {nombres_ganadores} con {ganador['puntos']} puntos!")
        else:
            print(f"\n¡El ganador de esta partida es {ganador['nombre']} con {ganador['puntos']} puntos!")
    else:
        print("\nNo hubo jugadores en esta partida.")


# --- FUNCION PRINCIPAL DE LA PARTIDA ---

def iniciar_partida(num_jugadores, frases_seleccionadas):
    """Inicia y gestiona una partida."""
    if not frases_seleccionadas:
        print("No hay frases disponibles para jugar con la dificultad seleccionada.")
        return # Salir si no hay frases

    # 1. Crear jugadores
    jugadores = []
    nombres_usados = set()
    for i in range(num_jugadores):
        while True:
            nombre = input(f"Nombre del Jugador {i+1}: ").strip()
            if not nombre:
                 print("El nombre no puede estar vacio.")
            elif nombre in nombres_usados:
                 print(f"El nombre '{nombre}' ya esta en uso.")
            else:
                jugadores.append(crear_jugador(nombre))
                nombres_usados.add(nombre)
                break

    # 2. Seleccion de frase y estado inicial
    frase_a_adivinar = random.choice(frases_seleccionadas)
    estado_actual_frase = inicializar_estado_frase(frase_a_adivinar)
    letras_usadas = set()

    # 3. Bucle principal del juego
    indice_jugador_actual = 0
    partida_terminada = False
    es_individual = (num_jugadores == 1)

    while not partida_terminada:
        jugador_activo = jugadores[indice_jugador_actual]
        turno_activo = True # Puede realizar acciones en su turno

        mostrar_estado_juego(jugador_activo, estado_actual_frase, letras_usadas)

        while turno_activo and not partida_terminada:
            opcion = obtener_opcion_principal(jugador_activo)

            if opcion == 1: # Comprar Vocal
                estado_actual_frase, exito_compra = comprar_vocal(
                    jugador_activo, frase_a_adivinar, estado_actual_frase, letras_usadas
                )
                turno_activo = False # Comprar vocal siempre termina la accion principal del turno
                if verificar_victoria(estado_actual_frase):
                    partida_terminada = True
                    print(f"\n¡{jugador_activo['nombre']} ha completado la frase al comprar una vocal!")

            elif opcion == 2: # Intentar Resolver
                gano = intentar_resolver(jugador_activo, frase_a_adivinar, estado_actual_frase)
                if gano:
                    partida_terminada = True
                    estado_actual_frase = frase_a_adivinar # Revelar frase
                turno_activo = False # Resolver siempre termina la accion

            elif opcion == 3: # Girar Ruleta
                sector_ruleta = girar_ruleta(es_individual) # Pasa si es individual o no
                resultado_ruleta = aplicar_resultado_ruleta(jugador_activo, sector_ruleta, jugadores)

                if isinstance(resultado_ruleta, int): # Toco puntos -> pedir consonante
                    estado_actual_frase, acerto_consonante = pedir_consonante(
                        jugador_activo, frase_a_adivinar, estado_actual_frase, letras_usadas, resultado_ruleta
                    )
                    if not acerto_consonante:
                        turno_activo = False # Fallar consonante termina el turno
                    # Si acerto, turno_activo sigue True, puede elegir otra accion
                    if verificar_victoria(estado_actual_frase):
                         partida_terminada = True
                         print(f"\n¡{jugador_activo['nombre']} ha completado la frase al adivinar una consonante!")

                elif resultado_ruleta == "TURNO_TERMINADO" or resultado_ruleta == "COMODIN_TERMINADO":
                    turno_activo = False # Ruleta/Comodin terminaron el turno

            # Mostrar estado si el turno continua y no ha terminado la partida
            if turno_activo and not partida_terminada:
                 mostrar_estado_juego(jugador_activo, estado_actual_frase, letras_usadas)

        # --- Fin del Turno ---
        if not partida_terminada:
            print(f"\n--- Fin del turno de {jugador_activo['nombre']} ---")
            indice_jugador_actual = (indice_jugador_actual + 1) % num_jugadores
            time.sleep(2)

    # 4. Fin de la partida
    print("\nMostrando frase completa:")
    print(frase_a_adivinar)
    finalizar_partida(jugadores)

# --- MENU PRINCIPAL ---

def mostrar_menu_principal():
    print("\n===== RUEDA DE LA FORTUNA =====")
    print("1. Jugar Nueva Partida")
    print("2. Ver Clasificacion")
    print("3. Salir")
    print("==============================")
    while True:
        opcion = input("Elige una opcion: ")
        if opcion in ["1", "2", "3"]:
            return int(opcion)
        else:
            print("Opcion invalida.")

def elegir_dificultad():
    print("\nElige la dificultad:")
    print("1. Facil")
    print("2. Medio")
    print("3. Dificil")
    while True:
        opcion = input("Tu eleccion (1, 2, 3): ")
        if opcion == "1":
            return ARCHIVO_FRASES_FACIL
        elif opcion == "2":
            return ARCHIVO_FRASES_MEDIO
        elif opcion == "3":
            return ARCHIVO_FRASES_DIFICIL
        else:
            print("Opcion invalida.")

def mostrar_clasificacion_pantalla():
    print("\n--- CLASIFICACION GENERAL ---")
    clasificacion = cargar_clasificacion()
    if not clasificacion:
        print("Aun no hay nadie en la clasificacion.")
    else:
        # Mostrar los N mejores (ya estan ordenados al cargar)
        for i, entrada in enumerate(clasificacion[:MAX_CLASIFICACION]):
            print(f"{i+1}. {entrada['nombre']} - {entrada['puntos']} puntos")
    print("---------------------------")
    input("\nPresiona Enter para volver al menu...")


# --- BLOQUE PRINCIPAL DE EJECUCION ---

if __name__ == "__main__":
    # Asegurarse que los archivos de frases existen
    generar_archivos_frases_si_no_existen()

    while True:
        opcion_menu = mostrar_menu_principal()

        if opcion_menu == 1: # Jugar
            # Pedir numero de jugadores
            while True:
                try:
                    num_jugadores = int(input("Introduce el numero de jugadores (1 o mas): "))
                    if num_jugadores >= 1:
                        break
                    else:
                        print("Debe haber al menos 1 jugador.")
                except ValueError:
                    print("Por favor, introduce un numero valido.")

            # Elegir dificultad y cargar frases
            archivo_dificultad = elegir_dificultad()
            frases_juego = cargar_frases(archivo_dificultad)

            # Iniciar la partida si hay frases
            if frases_juego:
                iniciar_partida(num_jugadores, frases_juego)
            else:
                print(f"No se pudieron cargar frases de '{archivo_dificultad}'. No se puede iniciar la partida.")


        elif opcion_menu == 2: # Ver Clasificacion
            mostrar_clasificacion_pantalla()

        elif opcion_menu == 3: # Salir
            print("¡Gracias por jugar! Adios.")
            break