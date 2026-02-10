import discord
from config import OWNER_ID

def make_embed(title, description, image_url=None, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    if image_url:
        embed.set_image(url=image_url)
    embed.set_footer(text="Bot hecho por zJonch")
    return embed
