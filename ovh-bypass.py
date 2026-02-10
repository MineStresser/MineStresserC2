from scapy.all import *

# Dirección IP de origen falsificada (Cloudflare)
src_ip = "173.245.49.100"

# Dirección IP de destino
dst_ip = "46.105.222.228"  # Reemplaza con la IP que deseas probar

# Puerto destino
dst_port = 53  # Reemplaza con el puerto que deseas probar

# Crear un paquete UDP
packet = IP(src=src_ip, dst=dst_ip)/UDP(dport=dst_port, sport=12345)/Raw(load="Hola, mundo!")

# Enviar el paquete
send(packet)
