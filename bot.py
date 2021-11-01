import discord
from discord.ext import commands

client = commands.Bot("/")

@client.event
async def on_ready( ):
           print("Bot is ready")
