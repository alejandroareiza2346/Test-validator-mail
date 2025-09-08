# Programa para validar números de celular de Colombia
# Autor: Alejandro
# Fecha: 2025-09-07

import re

def validar_numero_colombia(numero):
    """
    Valida si el número de celular colombiano es correcto.
    Debe tener 10 dígitos, iniciar con 3 y los siguientes 9 ser dígitos.
    """
    # Expresión regular: ^3\d{9}$
    patron = r'^3\d{9}$'
    return bool(re.match(patron, numero))

if __name__ == "__main__":
    # Ejemplos de números para probar la función
    ejemplos = [
        "3123456789",   # Válido
        "312345678",    # Inválido: solo 9 dígitos
        "4123456789",   # Inválido: no inicia con 3
        "31234567890",  # Inválido: 11 dígitos
        "3a23456789",   # Inválido: contiene letra
        "3000000000",   # Válido
    ]

    # Probar cada ejemplo y mostrar el resultado
    for numero in ejemplos:
        if validar_numero_colombia(numero):
            print(f"{numero}: Válido")
        else:
            print(f"{numero}: Inválido")
