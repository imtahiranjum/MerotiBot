from discord.ext import commands
import random
from Functions.translator import microsoft_translator, microsoft_translator_quote_ur, microsoft_translator_ur


class Translation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("t",), help="Translates text to a language. Example: mt Arabic 'How are you?'")
    async def translate(self, ctx, to_lang, text):
        await ctx.send(embed=microsoft_translator(ctx=ctx, text_to_translate=text, to_language=to_lang))

    @commands.command(aliases=("tu",), help="Translates text from a language to Urdu Example: mu 'How are you?'")
    async def translate_ur(self, ctx, text):
        await ctx.send(embed=microsoft_translator_ur(ctx=ctx, text_to_translate=text))

    @commands.command(aliases=("tq",), help="Gives a random quote with urdu translation")
    async def translated_quote(self, ctx):
        sequence = ["i", "q", "j", "t", "g"]
        await ctx.send(embed=microsoft_translator_quote_ur(ctx=ctx, quote_of=random.choice(sequence)))


def setup(bot):
    bot.add_cog(Translation(bot))
