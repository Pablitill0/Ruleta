#Pedir una letrita
#importar actulizar_estado_frase
from actualizar_estado_frase.py import *

def pedir_letra(letras_intentadas, frase, estado_frase):
    letra = ''
    while True:
        letra = input('Introduce una letra: ')
        if len(letra) != 1 or isalpha(letra):
            print('Introduce una unica letra')
            continue
        if letra in letras_intentadas:
            print('Esa letra ya se ha intentado, elige otra.')
            continue
        elif letra in frase:
            #Posible problema actulizar_estado_frase puede tener distinto nombre
            estado_frase = actualizar_estado_frase(frase, estado_frase, letra)
            print(f"¡Bien! La frase ahora es: {phrase_state}")
        else:
            print("Letra incorrecta.")
        letras_intentadas.add(letra)
