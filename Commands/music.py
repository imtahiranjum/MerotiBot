from discord.ext import commands
import discord
import asyncio
from Functions.music import YTDLSource, join


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx):
        await join(ctx)

    @commands.command(name='play_song', aliases=("ps",), help='To play song')
    async def play(self, ctx, url):
        try:
            await join(ctx)
        except ConnectionError:
            print("Already Connected")
        try:
            async with ctx.typing():
                await ctx.message.add_reaction("👍")
                server = ctx.message.guild
                voice_channel = server.voice_client
                filename = await YTDLSource.from_url(url, loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(source=filename))
                filename = str(filename).format()
                filename = filename.replace("_", " ")
                filename = filename.split("-")[0:-1]
                filenameJoined = ""
                filenameJoined = filenameJoined.join(filename)

                await ctx.send('Now playing:- \n' + "```" + filenameJoined + "```")
        except ConnectionError:
            await ctx.send("Something is wrong :( ")

    @commands.command(name='play_song_loop', aliases=("psl",), help='To play one song in loop for number of times')
    async def playloop(self, ctx, times, url):
        global message
        try:
            await join(ctx)
        except ConnectionError:
            print("Already Connected")
        try:
            channel = ctx.message.author.voice.channel
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_connected():
                pass
            else:
                await channel.connect()
            async with ctx.typing():
                await ctx.message.add_reaction("👍")
                server = ctx.message.guild
                voice_channel = server.voice_client
                filename = await YTDLSource.from_url(url, loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(source=filename))
                filenameS = filename
                filename = str(filename).format()
                filename = filename.replace("_", " ")
                filename = filename.split("-")[0:-1]
                filenameJoined = ""
                filenameJoined = filenameJoined.join(filename)
                voice_client = ctx.message.guild.voice_client

                await ctx.send('Now playing:- \n' + "```" + filenameJoined + "```" + "\n" + str(int(times)) + " times")
            for x in range(int(times)):
                condition = True
                while condition:
                    if voice_client.is_paused() or voice_client.is_playing():
                        pass
                    else:
                        condition = False
                    await asyncio.sleep(1)
                voice_channel.play(discord.FFmpegPCMAudio(source=filenameS))
                if x == 0:
                    message = await ctx.message.reply(f"Remaining loops: {int(times) - x - 1}")
                    print(message)
                else:
                    await message.edit(content=f"Remaining loops: {int(times) - x - 1}")

        except Exception as e:
            print(f"Error occurred: {e}")
            await ctx.message.add_reaction("👎")
            await ctx.reply("Something is wrong :( ")

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.message.add_reaction("▶")
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.message.add_reaction("⏸")
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction("⏹")
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='disconnect', help='Disconnect the bot from channel')
    async def disconnect(self, ctx):
        try:
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_connected:
                await voice_client.disconnect()
                await ctx.message.add_reaction("☑")
        except ConnectionError:
            await ctx.reply("The bot is not connected to a voice channel at the moment.")


def setup(bot):
    bot.add_cog(Music(bot))
