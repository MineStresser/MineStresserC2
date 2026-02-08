import os
try:
    import colorama
except ModuleNotFoundError:
    os.system('pip install colorama')
from colorama import Fore
try:
    import pyfiglet
except ModuleNotFoundError:
    os.system('pip install pyfiglet')
import time
os.system("clear")

lista_numeros = ["1" , "2" , "3" , "4" , "5"]

while True:
	os.system("clear")
	os.system("pyfiglet --color=RED MineStresserC2")
	print(Fore.RED + "[1] IP L4")
	print(Fore.RED + "[2] Ping Checker MCPE")
	print(Fore.RED + "[3] MCBOT 0.14.x")
	print("")
	
	player = input(Fore.RED + "Select Options: ")
	
	if player == '2':
		os.system("clear")
		os.system("pyfiglet --color=RED MineStresserC2")
		player_4_ip = input(Fore.RED + "IP: ")
		player_4_port = input(Fore.RED + "Port: ")
		time.sleep(1)
		os.system("clear")
		os.system("pyfiglet --color=RED MineStresserC2")
		os.system(f"python ping.py {player_4_ip} -p {player_4_port}")
		
	if player == '3':
		os.system("clear")
		os.system("pyfiglet --color=RED MineStresserC2")
		player_3_ip = input(Fore.RED + "IP: ")
		player_3_port = input(Fore.RED + "Port: ")
		player_3_bots = input(Fore.RED + "How Many Bots You Want: ")
		time.sleep(1)
		os.system("clear")
		os.system("pyfiglet --color=RED MineStresserC2")
		print(Fore.BLUE + f"Running MCBot: {player_4_ip} {player_4_port}")
		os.system(f"python mcbot.py {player_3_ip} {player_3_port} {player_3_bots}")
		
	if player == '1':
		os.system("clear")
		os.system("python stress.py")		
		
