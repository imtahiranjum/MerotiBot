from discord.ext import commands
from Functions.database import server_collection, get_response
import discord


class Management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="stats enable", aliases=("se", ), help="Adds stats to the server")
    async def stats_enable(self, ctx):

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }
        category_stats = await ctx.guild.create_category(name="↢↢↢↢『SERVER STATS』↣↣↣↣")
        total_members = ctx.guild.member_count
        bot_counter = 0
        try:
            for x in ctx.guild.members:
                if x.bot:
                    bot_counter = bot_counter + 1
        except Exception as e:
            ctx.reply(f"Couldn't count bots because following error occurred:-\n{e}")

        members_channel = await ctx.guild.create_voice_channel(name=f"『🤵』 Members: {total_members}",
                                                               overwrites=overwrites, category=category_stats)
        bots_channel = await ctx.guild.create_voice_channel(name=f"『🤖』 Bots: {bot_counter}", overwrites=overwrites,
                                                            category=category_stats)
        find_server = {"guild id": ctx.guild.id}
        enable_stats = {"$set": {"stats status": True, "members channel id": members_channel.id,
                                 "bots channel id": bots_channel.id, "category stats id": category_stats.id}}
        if find_server is not None:
            server_collection.update_one(find_server, enable_stats)
        await ctx.reply(f"Successfully enabled stats")

    @commands.has_permissions(administrator=True)
    @commands.command(name="stats disable", aliases=("sd", ), help="Removes stats from the server")
    async def stats_disable(self, ctx):
        global find
        global category_stats_id
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "category stats id": 1}):
            category_stats_id = get_response(x)
            find = x

        try:
            stats_category = discord.Guild.get_channel(ctx.guild, int(category_stats_id))
            for channel in stats_category.voice_channels:
                await channel.delete()

            for channel in stats_category.text_channels:
                await channel.delete()

            await stats_category.delete()

        except Exception as e:
            await ctx.reply(f"Error Occurred: {e}")

        disable_stats = {"$set": {"stats status": False, "members channel id": 0,
                                  "bots channel id": 0, "category stats id": 0}}
        if find is not None:
            server_collection.update_one(find, disable_stats)
        await ctx.reply(f"Successfully disabled stats")

    @commands.has_permissions(administrator=True)
    @commands.command(name="change_prefix", aliases=("cp",), help="Changes the prefix for server")
    async def change_prefix(self, ctx, prefix):
        find_server = {"guild id": ctx.guild.id}
        set_prefix = {"$set": {"command prefix": f"{prefix}"}}
        if find_server is not None:
            server_collection.update_one(find_server, set_prefix)
        await ctx.reply(f"Successfully changed prefix to ```{prefix}```")

    @commands.command(name="change date channel", aliases=("cdatec",),
                      help="Changes bot date Channel for this server : copy id of channel and paste after command")
    @commands.has_permissions(administrator=True)
    async def change_date_channel(self, ctx, date_channel_id):
        find_server = {"guild id": ctx.guild.id}
        set_date_channel = {"$set": {"date channel": int(date_channel_id)}}
        if find_server is not None:
            server_collection.update_one(find_server, set_date_channel)
            await ctx.reply(f"Quote Channel Changed to {date_channel_id}")

    @commands.command(name="change day channel", aliases=("cdayc",),
                      help="Changes bot Time Channel for this server : copy id of channel and paste after command")
    @commands.has_permissions(administrator=True)
    async def change_day_channel(self, ctx, day_channel_id):
        find_server = {"guild id": ctx.guild.id}
        set_day_channel = {"$set": {"day channel": int(day_channel_id)}}
        if find_server is not None:
            server_collection.update_one(find_server, set_day_channel)
            await ctx.reply(f"Day Channel Changed to {day_channel_id}")

    @commands.command(name="change history channel", aliases=("chc",),
                      help="Changes History Channel for this server : copy id of channel and paste after command")
    @commands.has_permissions(administrator=True)
    async def change_history_channel(self, ctx, history_channel_id):
        find_server = {"guild id": ctx.guild.id}
        set_history_channel = {"$set": {"history channel": int(history_channel_id)}}
        if find_server is not None:
            server_collection.update_one(find_server, set_history_channel)
            await ctx.reply(f"History Channel Changed to {history_channel_id}")

    @commands.command(name="change quote channel", aliases=("cqc",),
                      help="Changes Quote Channel for this server : copy id of channel and paste after command")
    @commands.has_permissions(administrator=True)
    async def change_quote_channel(self, ctx, quote_channel_id):
        find_server = {"guild id": ctx.guild.id}
        set_quote_channel = {"$set": {"quote channel": int(quote_channel_id)}}
        if find_server is not None:
            server_collection.update_one(find_server, set_quote_channel)
            await ctx.reply(f"Quote Channel Changed to {quote_channel_id}")


def setup(bot):
    bot.add_cog(Management(bot))
