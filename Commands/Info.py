import datetime
import discord
from discord.ext import commands
from Functions.database import server_collection


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help="Displays your ping")
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!  🕐 ", timestamp=datetime.datetime.utcnow(), color=0xdb0000)
        embed.set_footer(text=f"✔ Request by: {ctx.author.name}")
        embed.add_field(name="  ⌛  **PING** in milliseconds:- "
                        , value=f"  ◾ {round(self.bot.latency * 1000, ndigits=4)}ms", inline=False)
        embed.add_field(name="  ⌛  **PING** in seconds:- "
                        , value=f"  ◾ {round(self.bot.latency, ndigits=4)}", inline=False)

        await ctx.reply(embed=embed, mention_author=True)
        print("PINGED")

    @commands.command(name="server_info", aliases=["si", ], description="Shows info about the current server.")
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description=" ")
        roleCount = len(ctx.guild.roles)
        bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        embed.set_thumbnail(url=str(ctx.guild.icon_url))

        embed.add_field(name=f"Sever ID: {ctx.guild.id}", value="⠀", inline=False)
        embed.add_field(name="Verification Level", value=str(ctx.guild.verification_level).capitalize(), inline=False)
        embed.add_field(name="Region", value=str(ctx.guild.region).capitalize(), inline=False)
        categories = ctx.guild.categories
        text_channels = ctx.guild.text_channels
        embed.add_field(name=f"Channels: ({len(categories) + len(text_channels)})",
                        value=f"Category: {len(categories)}\nText: {len(text_channels)}",
                        inline=False)
        embed.add_field(name="Server Owner", value=str(ctx.guild.owner.mention), inline=False)
        embed.add_field(name="Created On", value=ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                        inline=False)
        embed.add_field(name=f"Roles: ({len(ctx.guild.roles)})", value="⠀", inline=False)

        embed.set_footer(icon_url=str(ctx.author.avatar_url), text=f"Requested by {ctx.author.name}")

        await ctx.reply(embed=embed, mention_author=True)

    @commands.command(name="servercount", aliases=["gsc", ], description="Shows server counter of Meroti")
    async def servers(self, ctx):
        server_count = 0
        data = server_collection.find({}, {"_id": 0, "command prefix": 1})
        for _ in data:
            server_count = server_count + 1
        await ctx.reply(f"I am in {server_count} servers")

    @commands.command(name="avatar", aliases=["av", ], help="Displays the avatar of a member!", color=0x7289da)
    async def avatar(self, ctx, member: discord.Member):
        print(member)
        embed = discord.Embed(title=f"Avatar for {member.name}")
        embed.set_image(url=str(member.avatar_url))
        await ctx.reply(embed=embed)

    @commands.command(name="weather", aliases=("w",), help="Displays the weather "
                                                           "of the city")
    async def weather(self, ctx, city):
        embed = discord.Embed(title=f"Weather for {city}", timestamp=datetime.datetime.utcnow(), color=0xdb0000)
        embed.set_image(url=str("https://wttr.in/{}.png".format(city)))
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
