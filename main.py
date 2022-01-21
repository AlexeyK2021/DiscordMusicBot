import discord
from discord.ext import commands
from config import settings
from YouTubeTrack import *

IsAlreadyConnectedToChannel = False
bot = commands.Bot(settings['prefix'])
DL = youtube_dl.YoutubeDL
queue = []


def main():
    @bot.command('hello')
    async def hello(ctx):
        author = ctx.message.author
        hello_text = "Hello " + author.mention + " :grinning:"
        await ctx.send(ctx=ctx, text=hello_text)

    @bot.command('play')
    async def play(ctx, url):
        global IsAlreadyConnectedToChannel, voice_channel, vc, playing_now
        if not IsAlreadyConnectedToChannel:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()
            IsAlreadyConnectedToChannel = True

        if "youtu.be" or "youtube.com" in url:
            queue.append(YouTubeTrack(url))
        await run_music(ctx)
        # duration = int(info['duration'])
        # hours = duration // 3600
        # hours_str = "0" + str(hours) if hours < 10 else str(hours)
        # mins = duration // 60
        # mins_str = "0" + str(mins) if mins < 10 else str(mins)
        # secs = duration % 60
        # secs_str = "0" + str(secs) if secs < 10 else str(secs)
        # duration_str = hours_str + ":" + mins_str + ":" + secs_str
        # embed.add_field(name="Duration", value=duration_str)

        # else:
        #     URL = url  # для тестов
        # try:
        #     if not vc.is_playing():
        #         playing_now = queue.pop(0)
        #         vc.play(discord.FFmpegPCMAudio(playing_now.music_url), after=play)
        #
        #     embed = discord.Embed(
        #         title="Now Playing from YouTube",
        #         color=discord.Color.random(seed=13582)
        #     )
        #     embed.set_thumbnail(url=playing_now.image_link)
        #     embed.add_field(name="Channel", value=playing_now.channel)
        #     embed.add_field(name="Track", value=playing_now.name)
        #     embed.add_field(name="Duration", value=playing_now.get_duration)
        #     await ctx.send(embed=embed)
        #
        # except Exception:
        #     print("Player Error")

    # def findMP3(path):
    #     for file in os.listdir(path):
    #         filename, file_extension = os.path.splitext(file)
    #         if file_extension == ".mp3":
    #             queue.append(file)

    async def run_music(ctx):
        global playing_now, vc
        if not vc.is_playing():
            playing_now = queue.pop(0)
            vc.play(source=discord.FFmpegPCMAudio(playing_now.music_url))

            embed = discord.Embed(
                title="Now Playing from YouTube",
                color=discord.Color.random()
            )
            embed.set_thumbnail(url=playing_now.image_link)
            embed.add_field(name="Channel", value=playing_now.channel)
            embed.add_field(name="Track", value=playing_now.name)
            embed.add_field(name="Duration", value=playing_now.get_duration())
            await ctx.send(embed=embed)

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
