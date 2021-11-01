import discord
import youtube_dl
from discord import FFmpegPCMAudio
from discord.ext import commands
import vlc
import pafy
from discord.utils import get
from youtube_dl import YoutubeDL

from bot import client
from config import settings

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

@bot.command('play')
async def play(ctx):
    voicechannel = discord.utils.get(ctx.guild.channels, name='queue')
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio("Def Leppard - Hysteria (Radio Edit).mp3"))


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
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command('leave')
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command('testing')
async def testing(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


bot.run(settings['token'])
