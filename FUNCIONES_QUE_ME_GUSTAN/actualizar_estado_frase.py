import random
import time

"""
# Actualiza el estado de la frase (muestra las letras adivinadas)
def update_phrase_state(phrase, phrase_state, guessed_letter):
    updated_phrase_state = ""
    for i in range(len(phrase)):
        if phrase[i] == guessed_letter:
            updated_phrase_state += guessed_letter
        elif phrase[i] == " ":
            updated_phrase_state += " "
        else:
            updated_phrase_state += phrase_state[i]
    return updated_phrase_state
"""
#La primera vez que se le llama 
def actualizar_estado_frase(frase_original, estado_actual_frase, letra_adivinada):

    nuevo_estado_frase = ""  # Inicializa la cadena para el nuevo estado
    for i in range(len(frase_original)):
        # Si la letra en la frase original coincide con la letra adivinada
        if frase_original[i] == letra_adivinada:
            nuevo_estado_frase += letra_adivinada  # Añade la letra revelada
        else:
            # Mantiene el carácter que ya estaba en el estado actual
            # (puede ser un '_' u otra letra ya revelada)
            nuevo_estado_frase += estado_actual_frase[i]
    # Devuelve la cadena con el estado actualizado de la frase
    return nuevo_estado_frase

