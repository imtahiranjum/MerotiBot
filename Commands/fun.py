import asyncio
import datetime
import discord
from art import randart, text2art
from discord.ext import commands
import random
from Functions.misc import text_converter_random, list_fonts
from Functions import strings


class MiscCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="g", help="Displays Meroti's attitude!")
    async def g(self, ctx):
        await ctx.channel.send("جی بھائی؟ کوئی مسئلہ؟")

    @commands.command(name="speak", help="Meroti will send something")
    async def speak(self, ctx):
        async with ctx.typing():
            await ctx.reply(random.choice(strings.answer_words))
            await asyncio.sleep(9)
            await ctx.send(f"{str(randart())}")

    @commands.command(name="txtconvertrandom", aliases=("tcr",), help="Converts your text to art! Example: tcr 'text'")
    async def text_converter_random(self, ctx, text):
        await ctx.send(f"```{text_converter_random(text)}```")

    @commands.command(name="txtconvert", aliases=("tc",), help="Converts your text to art into "
                                                               "style you specify! Example: tcr 'You' Style1")
    async def text_converter(self, ctx, text, font):
        await ctx.send(f"```{text2art(text=text, font=font)}```")

    @commands.command(name="listfonts", aliases=("lf",), help="Displays list of fonts "
                                                              "available to convert your text")
    async def list_fonts(self, ctx):
        await ctx.send(f"```{list_fonts()}```")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
