import datetime
import discord
import operator
from discord.ext import commands
from Functions.misc import pagify
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

    @commands.command(aliases=["whoplay", "wp", "pg"])
    @commands.guild_only()
    async def whoplays(self, ctx, *, game: str):
        """Shows a list of all the people playing a game."""
        if len(game) <= 2:
            await ctx.send("You need at least 3 characters.")
            return

        member_list = []
        count_playing = 0
        for member in ctx.guild.members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            # Prevents searching through statuses
            if activity := discord.utils.get(member.activities, type=discord.ActivityType.playing):
                if game.lower() in activity.name.lower():
                    member_list.append(member)
                    count_playing += 1

        if count_playing == 0:
            await ctx.send("No one is playing this game.")
        else:
            sorted_list = sorted(member_list, key=lambda x: getattr(x, "name").lower())
            playing_game = ""
            for member in sorted_list:
                playing_game += "▸ {} ({})\n".format(member.name, member.activity.name)
            embed_list = []
            in_pg_count = 0

            for page in pagify(playing_game, delims=["\n"], page_length=400):
                in_page = page.count("▸")
                in_pg_count = in_pg_count + in_page
                title = f"These are the people who are playing {game}:\n"
                em = discord.Embed(description=page, colour=ctx.author.colour)
                em.set_footer(text=f"Showing {in_pg_count}/{count_playing}")
                em.set_author(name=title)
                embed_list.append(em)

            if len(embed_list) == 1:
                return await ctx.send(embed=em)

    @commands.command(aliases=["cg", "wpw"])
    @commands.guild_only()
    async def cgames(self, ctx: commands.Context):
        """Shows the currently most played games"""
        freq_list = {}
        for member in ctx.guild.members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            # This should ignore things that aren't under playing activity type
            if activity := discord.utils.get(member.activities, type=discord.ActivityType.playing):
                if activity.name not in freq_list:
                    freq_list[activity.name] = 0
                freq_list[activity.name] += 1

        sorted_list = sorted(freq_list.items(), key=operator.itemgetter(1), reverse=True)

        if not freq_list:
            await ctx.send("Surprisingly, no one is playing anything.")
        else:
            # create display
            msg = ""
            max_games = min(len(sorted_list), 10)
            for i in range(max_games):
                game, freq = sorted_list[i]
                msg += "▸ {}: __{}__\n".format(game, freq_list[game])

            em = discord.Embed(description=msg, colour=ctx.author.colour)
            em.set_author(name="These are the server's most played games at the moment:")
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Info(bot))
