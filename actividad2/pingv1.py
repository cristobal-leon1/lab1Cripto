import sys
import time
import datetime
import struct
from scapy.all import IP, ICMP, send

# Variables globales para timestamp personalizado
custom_timestamp_base = 0x6604_0000_0000_0000  # Timestamp base personalizado
timestamp_increment = 1  # Incremento para cada paquete enviado

def generar_custom_timestamp():
    """
    Genera un timestamp personalizado basado en el timestamp base y el incremento.
    """
    global custom_timestamp_base, timestamp_increment
    timestamp = custom_timestamp_base
    custom_timestamp_base += timestamp_increment
    return timestamp

def enviar_caracter_icmp(caracter, ip_destino, id_paquete, secuencia_paquete):
    """
    Función que envía un carácter en un paquete ICMP request individual.
    :param caracter: str, el carácter a enviar
    :param ip_destino: str, la dirección IP destino
    :param id_paquete: int, el identificador del paquete
    :param secuencia_paquete: int, el número de secuencia del paquete
    """
    # Generar timestamp personalizado
    timestamp = generar_custom_timestamp()

    # Guardar el caracter oculto
    caracter_oculto = caracter

    # Datos hex luego del caracter oculto
    datos_hex = "00000000000000101112131415161718191a1b1c1d1e1f202122232425262728292a1b2c2d2e2f3031323334353637"

    # Obtener el timestamp como bytes (8 bytes)
    timestamp_bytes = struct.pack("!Q", timestamp)

    # Crear datos ICMP con el primer caracter oculto del texto de entrada, timestamp y datos hexadecimales
    datos_icmp = timestamp_bytes + bytes([ord(caracter_oculto)]) + bytes.fromhex(datos_hex)

    # Crear el paquete ICMP echo request con timestamp y datos
    paquete_icmp = IP(src="127.0.0.1", dst=ip_destino, id=id_paquete, ttl=64) / ICMP(type=8, code=0, id=id_paquete, seq=secuencia_paquete) / datos_icmp

    # Enviar paquete
    send(paquete_icmp, verbose=False)

    # Mostrar caracter enviado y timestamp
    print(f"Enviado: {caracter_oculto}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 enviar_caracteres_icmp.py <texto>")
        sys.exit(1)

    # Obtener el texto a enviar desde los argumentos de línea de comandos
    texto = sys.argv[1]

    # Dirección IP destino (loopback)
    ip_destino = "127.0.0.1"

    # Iniciar el ID de paquete en 1
    id_paquete = 1

    # Iniciar el número de secuencia en 1
    secuencia_paquete = 1

    # Enviar cada carácter del texto
    for caracter in texto:
        # Enviar el carácter ICMP
        enviar_caracter_icmp(caracter, ip_destino, id_paquete, secuencia_paquete)

        # Incrementar el ID de paquete
        id_paquete += 1

        # Incrementar el número de secuencia
        secuencia_paquete += 1

        # Esperar 1 segundo antes de enviar el siguiente carácter
        time.sleep(1)
