import random
import time

# Función para girar la ruleta
def spin_wheel():
    # La ruleta tiene diferentes valores y opciones
    sectors = [25, 50, 75, 100, 150, 200, "BANKRUPT", "LOSE_TURN", "ME_LO_QUEDO", "SE_LO_DOY"]
    return random.choice(sectors)

