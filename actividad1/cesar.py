import sys

def cifrar_cesar(texto, corrimiento):
    texto_cifrado = ''
    for caracter in texto:
        # Verificar si el caracter es una letra
        if caracter.isalpha():
            # Obtener el código ASCII del caracter
            codigo = ord(caracter)
            # Aplicar el corrimiento y ajustar según el rango de letras mayúsculas o minúsculas
            if caracter.islower():
                codigo_cifrado = (codigo - ord('a') + corrimiento) % 26 + ord('a')
            elif caracter.isupper():
                codigo_cifrado = (codigo - ord('A') + corrimiento) % 26 + ord('A')
            # Convertir el código ASCII cifrado de nuevo a caracter
            caracter_cifrado = chr(codigo_cifrado)
            # Agregar el caracter cifrado al texto cifrado
            texto_cifrado += caracter_cifrado
        else:
            # Si el caracter no es una letra, simplemente agregarlo sin cifrar
            texto_cifrado += caracter
    return texto_cifrado

if len(sys.argv) != 3:
    print("Uso: python3 cifrado_cesar.py <texto_a_cifrar> <corrimiento>")
    sys.exit(1)

# Obtener los argumentos de la línea de comandos
texto_a_cifrar = sys.argv[1]
corrimiento = int(sys.argv[2])

# Llamar a la función para cifrar el texto
texto_cifrado = cifrar_cesar(texto_a_cifrar, corrimiento)

# Mostrar el texto cifrado
print(texto_cifrado)
