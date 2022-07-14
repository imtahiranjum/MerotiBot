from discord.ext import commands
from Functions.webscrap import quote_scraped, quote_scraped_islamic, \
    urdu_quote_scraped, taymiyah_quote_scraped, al_jawzi_quote_scraped, ghazaali_quote_scraped


class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command("quote", aliases=("q",), help="Displays famous quotes")
    async def quote(self, ctx):
        await ctx.channel.send(quote_scraped())

    @commands.command("quoteislamic", aliases=("qi",), help="Displays Islamic quotes")
    async def quote_islamic(self, ctx):
        await ctx.channel.send(quote_scraped_islamic())

    @commands.command("quoteurdu", aliases=("qu",), help="Displays famous Urdu quotes")
    async def quote_urdu(self, ctx):
        await ctx.channel.send(urdu_quote_scraped())

    @commands.command("quotetaymiyah", aliases=("qt",), help="Displays famous quotes of Ibn e Taymiyah")
    async def quote_taymiyah(self, ctx):
        await ctx.channel.send(taymiyah_quote_scraped())

    @commands.command("quotejawzi", aliases=("qj",), help="Displays famous quotes of Ibn e Jawzi")
    async def quote_jawzi(self, ctx):
        await ctx.channel.send(al_jawzi_quote_scraped())

    @commands.command("quoteghazali", aliases=("qg",), help="Displays famous quotes of Imam Al-Ghazaali")
    async def quote_ghazali(self, ctx):
        await ctx.channel.send(ghazaali_quote_scraped())


def setup(bot):
    bot.add_cog(Quotes(bot))
