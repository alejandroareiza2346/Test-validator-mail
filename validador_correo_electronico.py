# Programa para validar correos electrónicos
# Autor: Alejandro
# Fecha: 2025-09-07

import re

def validar_correo_electronico(correo):
    """
    Valida si el correo electrónico tiene un formato correcto usando expresiones regulares.
    El formato básico es: texto@texto.dominio
    """
    # Expresión regular para correo electrónico
    patron = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, correo))

if __name__ == "__main__":
    # Ejemplos de correos para probar la función
    ejemplos = [
        "usuario@dominio.com",      # Válido
        "usuario@dominio.co",       # Válido
        "usuario@dominio",          # Inválido: falta dominio
        "usuario@.com",             # Inválido: falta nombre de dominio
        "@dominio.com",             # Inválido: falta nombre de usuario
        "usuario@dominio.c",        # Inválido: dominio muy corto
        "usuario.nombre@dominio.com", # Válido
        "usuario-nombre@dominio.com", # Válido
    ]

    # Probar cada ejemplo y mostrar el resultado
    for correo in ejemplos:
        if validar_correo_electronico(correo):
            print(f"{correo}: Válido")
        else:
            print(f"{correo}: Inválido")
