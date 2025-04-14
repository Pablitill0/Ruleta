import random
import time

"""# Verifica si el jugador ha ganado
def check_win_condition(phrase_state):
    # Si no hay más guiones bajos, la frase ha sido adivinada completamente
    return "_" not in phrase_state
"""

def check_win_condition(phrase_state):
    resultado = phrase_state.find("_")  # Busca el primer guion bajo en la frase
    if resultado == -1:
        return True
    else:
        return False