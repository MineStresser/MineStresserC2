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
	os.system("pyfiglet --color=RED 𝕄𝕚𝕟𝕖𝕋𝕖𝕒𝕞ℍ𝟜ℂ𝕂")
	print(Fore.RED + "[1] IP L4")
	print(Fore.RED + "[2] Ping Checker MCPE")
	print("")
	print("Credit: MineGamerST")
	print("")
	
	player = input(Fore.RED + "Select Options: ")
	
	if player == '2':
		os.system("clear")
		os.system("pyfiglet --color=RED 𝕄𝕚𝕟𝕖𝕋𝕖𝕒𝕞ℍ𝟜ℂ𝕂")
		player_4_ip = input(Fore.RED + "IP: ")
		player_4_port = input(Fore.RED + "Port: ")
		time.sleep(1)
		os.system("clear")
		os.system("pyfiglet --color=RED 𝕄𝕚𝕟𝕖𝕋𝕖𝕒𝕞ℍ𝟜ℂ𝕂")
		os.system(f"python ping.py {player_4_ip} -p {player_4_port}")
		
	if player == '1':
		os.system("clear")
		os.system("python stress.py")		
		
