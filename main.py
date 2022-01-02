import sys
import time

import discord
import youtube_dl
from discord.ext import commands
from config import settings

IsAlreadyConnectedToChannel = False
bot = commands.Bot(settings['prefix'])
DL = youtube_dl.YoutubeDL

def main():
    @bot.command('hello')
    async def hello(ctx):
        author = ctx.message.author
        hello_text = "Hello " + author.mention + " :grinning:"
        await ctx.send(ctx=ctx, text=hello_text)

    @bot.command('play')
    async def play(ctx, url):
        global IsAlreadyConnectedToChannel, voice_channel, vc
        if not IsAlreadyConnectedToChannel:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()
            IsAlreadyConnectedToChannel = True
        ydl_opts = {'format': 'bestaudio'}
        if "youtu.be" in url:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
        else:
            URL = url  # для тестов
        # print(info)
        # embed = discord.Embed(
        #     title="Now Playing",
        #     description=info['title'],
        #     color=discord.Color.dark_blue()
        # )
        # embed.set_thumbnail(url=URL)

        # await ctx.send(embed=embed)
        try:
            if vc.is_playing():
                await stop(ctx)
            time.sleep(1)
            vc.play(discord.FFmpegPCMAudio(URL))
        except Exception:
            print("Player Error")

    # def findMP3(path):
    #     for file in os.listdir(path):
    #         filename, file_extension = os.path.splitext(file)
    #         if file_extension == ".mp3":
    #             queue.append(file)

    @bot.command('pause')
    async def pause(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @bot.command('resume')
    async def resume(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use !play command")

    @bot.command('stop')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
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
