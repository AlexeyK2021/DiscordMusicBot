import sys
import os
import discord
import youtube_dl
from discord.ext import commands
from config import settings

IsAlreadyConnectedToChannel = False
bot = commands.Bot(settings['prefix'])
DL = youtube_dl.YoutubeDL
NowPlaying = ""


def main():
    @bot.command('hello')  # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
    async def hello(ctx):  # Создаём функцию и передаём аргумент ctx.
        author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
        hello_text = "Hello " + author.mention + " :grinning:"
        await discordPrint(ctx=ctx, text=hello_text)

    async def discordPrint(text, ctx):
        await ctx.send(text)

    @bot.command('play')
    async def play(ctx, url):
        global IsAlreadyConnectedToChannel, voice_channel
        if not IsAlreadyConnectedToChannel:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()
            IsAlreadyConnectedToChannel = True
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
        print(info)
        embed = discord.Embed(
            title="Now Playing",
            description=info['title'],
            color=discord.Color.dark_blue()
        )
        await ctx.send(embed=embed)
        try:
            await vc.play(discord.FFmpegPCMAudio(URL))
        except Exception:
            print("Player Error")

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
        global IsAlreadyConnectedToChannel, voice_channel
        if not IsAlreadyConnectedToChannel:
            voice_channel = ctx.author.voice.channel
            IsAlreadyConnectedToChannel = True
            await voice_channel.connect()

    @bot.command('leave')
    async def leave(ctx):
        global IsAlreadyConnectedToChannel
        if IsAlreadyConnectedToChannel:
            IsAlreadyConnectedToChannel = False
            await ctx.voice_client.disconnect()

    bot.run(settings['token'])


if __name__ == "__main__":
    main()
