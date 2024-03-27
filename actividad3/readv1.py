import sys
import pyshark
from termcolor import colored

# Verificar si se proporciona un archivo pcapng como argumento
if len(sys.argv) != 2:
    print("Uso: python3 readv1.py <archivo.pcapng>")
    sys.exit(1)

# Obtener el nombre del archivo pcapng del argumento de la línea de comandos
pcap_file = sys.argv[1]

# Diccionario de palabras en español
with open("spanish_words.txt", "r", encoding="utf-8") as file:
    spanish_words = set(word.strip().lower() for word in file)

# Cargar el archivo pcapng
cap = pyshark.FileCapture(pcap_file)

# Lista para almacenar todos los textos cifrados
ciphertexts = []

# Iterar sobre todos los paquetes en el archivo
for packet in cap:
    # Verificar si es un paquete ICMP de tipo "request"
    if "ICMP" in packet and packet.icmp.type == "8":
        # Acceder a los dos primeros bytes del campo data_data de ICMP
        first_two_bytes_hex = packet.icmp.data_data[:2]
        
        # Convertir los dos primeros bytes de hexadecimal a una cadena de bytes
        bytes_data = bytes.fromhex(first_two_bytes_hex)
        
        # Convertir la cadena de bytes a texto y agregarlo a la lista
        message = bytes_data.decode('utf-8')
        ciphertexts.append(message)

# Iterar sobre los corrimientos de César de 0 a 25
for shift in range(26):
    # Aplicar el corrimiento de César a cada texto cifrado y agregarlo a la lista de resultados
    shifted_text = ''
    for text in ciphertexts:
        shifted_message = ''
        for char in text:
            if char.isalpha():
                shifted_char = chr(((ord(char.lower()) - 97 + shift) % 26) + 97)
                if char.isupper():
                    shifted_char = shifted_char.upper()
                shifted_message += shifted_char
            else:
                shifted_message += char
        shifted_text += shifted_message
        
    # Buscar palabras en español en el texto cifrado
    found_spanish_word = any(word.lower() in spanish_words for word in shifted_text.split())
    
    # Imprimir el texto cifrado en verde si se encontró al menos una palabra en español
    if found_spanish_word:
        print(colored(shifted_text, "green"), "ROT-", 26 - shift) # indica el corrimiento cesar(llave)
    else:
        print(shifted_text, "ROT-", 26 - shift)
