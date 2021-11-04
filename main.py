import os
import sys
import ffmpeg
import discord
import youtube_dl
from discord import FFmpegPCMAudio
from discord.ext import commands
import vlc
import pafy
from discord.utils import get
from youtube_dl import YoutubeDL

from config import settings

IsAlreadyConnectedToChannel = False
bot = commands.Bot(settings['prefix'])
DL = youtube_dl.YoutubeDL


@bot.command('hello')  # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx):  # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Hello, {author.mention}! :grinning: ')


# @bot.command('play')
# async def play(ctx, arg):
# try:
#     server = ctx.message.guild
#     voice_channel = server.voice_client
#     async with ctx.typing():
#         voice_channel.play(discord.FFmpegPCMAudio("ffmpeg.exe"))
#     await ctx.send('**Now playing:** {'+arg+"}")
# except:
#     await ctx.send("The bot is not connected to a voice channel.")

# print(ctx.message, arg)
# video = pafy.new(arg)
# best = video.getbest()
# playurl = best.url
# Instance = vlc.Instance()
# player = Instance.media_player_new()
# Media = Instance.media_new(playurl)
# Media.get_mrl()
# player.set_media(Media)
# player.play()
#
#     await ctx.send('playing ' + arg)
queue = []


@bot.command('play')
async def play(ctx):
    global IsAlreadyConnectedToChannel, voicechannel
    if IsAlreadyConnectedToChannel == False:
        voicechannel = ctx.author.voice.channel
        IsAlreadyConnectedToChannel = True
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio("Godsmack - When Legends Rise.mp3", executable="ffmpeg.exe"))


async def console():
    command = input()
    if command == "stop":
        await leave()
        sys.exit()


# def findMP3(path):
#     for file in os.listdir(path):
#         filename, file_extension = os.path.splitext(file)
#         if file_extension == ".mp3":
#             queue.append(file)


@bot.command('pause')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command('resume')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use !play command")


@bot.command('stop')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command('join')
async def join(ctx):
    global IsAlreadyConnectedToChannel, voicechannel
    if IsAlreadyConnectedToChannel == False:
        voicechannel = ctx.author.voice.channel
        IsAlreadyConnectedToChannel = True
        await voicechannel.connect()


@bot.command('leave')
async def leave(ctx):
    global IsAlreadyConnectedToChannel
    if IsAlreadyConnectedToChannel == True:
        IsAlreadyConnectedToChannel = False
        await ctx.voice_client.disconnect()


@bot.command('testing')
async def testing(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


bot.run(settings['token'])
