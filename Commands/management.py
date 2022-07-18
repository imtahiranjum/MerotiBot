from discord.ext import commands
from Functions.database import server_collection, get_response
from Functions.management import time_get
import discord


class Management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="stats enable", aliases=("es",), help="Enables Stats")
    async def stats_enable(self, ctx):
        global status
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "stats status": 1}):
            status = get_response(x)
            print(status)
        if status == "False":
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
            }
            category_stats = await ctx.guild.create_category(name="↢↢↢↢『SERVER STATS』↣↣↣↣")
            total_members = ctx.guild.member_count
            bot_counter = 0
            humans = 0
            try:
                for x in ctx.guild.members:
                    if x.bot:
                        bot_counter = bot_counter + 1
            except Exception as e:
                ctx.reply(f"Couldn't count bots because following error occurred:-\n{e}")
            humans = total_members - bot_counter
            members_channel = await ctx.guild.create_voice_channel(name=f"『🤵』 Members: {total_members}",
                                                                   overwrites=overwrites, category=category_stats)
            humans_channel = await ctx.guild.create_voice_channel(name=f"『🤵』 Humans: {humans}", overwrites=overwrites,
                                                                  category=category_stats)
            bots_channel = await ctx.guild.create_voice_channel(name=f"『🤖』 Bots: {bot_counter}", overwrites=overwrites,
                                                                category=category_stats)
            find_server = {"guild id": ctx.guild.id}
            enable_stats = {"$set": {"stats status": True, "members channel id": members_channel.id,
                                     "bots channel id": bots_channel.id, "humans channel id": humans_channel.id,
                                     "category stats id": category_stats.id}}
            if find_server is not None:
                server_collection.update_one(find_server, enable_stats)
                await ctx.reply(f"Successfully enabled stats")
        else:
            await ctx.reply(f"Stats are already enabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="stats disable", aliases=("ds",), help="Disables Stats")
    async def stats_disable(self, ctx):
        global status
        global category_stats_id
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "category stats id": 1}):
            category_stats_id = get_response(x)

        for y in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "stats status": 1}):
            status = get_response(y)

        if status == "True":
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
                                      "bots channel id": 0, "humans channel id": 0,
                                      "category stats id": 0}}
            find_server = {"guild id": ctx.guild.id}
            if find_server is not None:
                server_collection.update_one(find_server, disable_stats)
                await ctx.reply(f"Successfully disabled stats")
        else:
            await ctx.reply(f"Stats are already disabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="date day", aliases=("edd",), help="Enables day and date")
    async def day_date_enable(self, ctx):
        current_area_time = time_get("Asia/Karachi")
        date_for_automation = current_area_time.strftime("%d-%b-%Y")
        day_for_automation = current_area_time.strftime("%A")
        global status
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "time and date status": 1}):
            status = get_response(x)
            print(status)
        if status == "False":
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
            }
            category_for_day_date = await ctx.guild.create_category(name="↢↢↢↢↢↢『⏳⏲⏳』↣↣↣↣↣↣", position=0)
            day_channel = await ctx.guild.create_voice_channel(name=f"『📅』: {day_for_automation}",
                                                               overwrites=overwrites,
                                                               category=category_for_day_date)
            date_channel = await ctx.guild.create_voice_channel(name=f"『📆』: {date_for_automation}",
                                                                overwrites=overwrites,
                                                                category=category_for_day_date)

            find_server = {"guild id": ctx.guild.id}
            enable_day_date = {"$set": {"time and date status": True, "day channel id": day_channel.id,
                                        "date channel id": date_channel.id,
                                        "category day and date id": category_for_day_date.id}}
            if find_server is not None:
                server_collection.update_one(find_server, enable_day_date)
                await ctx.reply(f"Successfully enabled day and date in the server")
        else:
            await ctx.reply(f"Day and date is already enabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="day date disable", aliases=("ddd",), help="Disables day and date")
    async def day_date_disable(self, ctx):
        global status
        global category_day_date_id
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "category day and date id": 1}):
            category_day_date_id = get_response(x)

        for y in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "time and date status": 1}):
            status = get_response(y)

        if status == "True":
            try:
                day_date_category = discord.Guild.get_channel(ctx.guild, int(category_day_date_id))
                for channel in day_date_category.voice_channels:
                    await channel.delete()

                for channel in day_date_category.text_channels:
                    await channel.delete()

                await day_date_category.delete()

            except Exception as e:
                await ctx.reply(f"Couldn't do that due to some technical error! Try again later")
                print(f"Error occurred {e}")

            disable_day_date = {"$set": {"time and date status": False, "day channel id": 0,
                                         "date channel id": 0,
                                         "category day and date id": 0}}
            find_server = {"guild id": ctx.guild.id}
            if find_server is not None:
                server_collection.update_one(find_server, disable_day_date)
                await ctx.reply(f"Successfully disabled day and date from the server")
        else:
            await ctx.reply(f"Day and date is already disabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="quotes enable", aliases=("eq",), help="Enables daily quotes")
    async def quotes_enable(self, ctx):
        global status, category_info_id
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "daily quotes status": 1}):
            status = get_response(x)
            print(status)

        if status == "False":
            overwrites_text_channel = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            try:
                for y in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "category info id": 1}):
                    category_info_id = get_response(y)
                    print(status)
                category_info = discord.Guild.get_channel(ctx.guild, int(category_info_id))
            except Exception as e:
                print(f"Error in fetching category: {e} ")
            if category_info is None:
                category_info = await ctx.guild.create_category(name="↢↢↢↢↢『DailyDose』↣↣↣↣↣", position=0)
            quote_channel = await ctx.guild.create_text_channel(name=f"『📚』: Daily-Quotes",
                                                                overwrites=overwrites_text_channel,
                                                                category=category_info, news=True)
            find_server = {"guild id": ctx.guild.id}
            enable_stats = {"$set": {"daily quotes status": True, "quote channel id": quote_channel.id,
                                     "category info id": category_info.id}}
            if find_server is not None:
                server_collection.update_one(find_server, enable_stats)
                await ctx.reply(f"Successfully enabled daily quotes")
        else:
            await ctx.reply(f"Daily quotes are already enabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="quotes disable", aliases=("dq",), help="Disables daily quotes")
    async def quotes_disable(self, ctx):
        global status, history_channel_id, quote_channel_id, category_info_id
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "category info id": 1}):
            category_info_id = get_response(x)

        for y in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "daily quotes status": 1}):
            status = get_response(y)

        try:
            for history_channel in server_collection.find({"guild id": ctx.guild.id},
                                                          {"_id": 0, "history channel id": 1}):
                history_channel_id = get_response(history_channel)
        except Exception as e:
            print(f"Error occurred: {e}")
            history_channel_id = None

        try:
            for quote_channel in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "quote channel id": 1}):
                quote_channel_id = get_response(quote_channel)
        except Exception as e:
            print(f"Error occurred: {e}")
            quote_channel_id = None

        if status == "True":
            try:
                info_category = discord.Guild.get_channel(ctx.guild, int(category_info_id))
                if quote_channel_id != "0" or not None:
                    quote_channel = discord.Guild.get_channel(ctx.guild, int(quote_channel_id))
                if history_channel_id != "0" or not None:
                    history_channel = discord.Guild.get_channel(ctx.guild, int(history_channel_id))
                if info_category != "0" or not None:
                    for channel in info_category.text_channels:
                        if channel == quote_channel:
                            await channel.delete()

                if history_channel is None:
                    await info_category.delete()
                    category_info_id = 0

            except Exception as e:
                await ctx.reply(f"Error Occurred: {e}")

            disable_stats = {"$set": {"daily quotes status": False, "quotes channel id": 0,
                                      "category info id": int(category_info_id)}}
            find_server = {"guild id": ctx.guild.id}
            if find_server is not None:
                server_collection.update_one(find_server, disable_stats)
                await ctx.reply(f"Successfully disabled daily history")
        else:
            await ctx.reply(f"Daily history is already disabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="history enable", aliases=("eh",), help="Enable daily history")
    async def history_enable(self, ctx):
        global status, category_info_id, category_info
        for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "daily history status": 1}):
            status = get_response(x)
            print(status)
        if status == "False":
            overwrites_text_channel = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            try:
                for y in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "category info id": 1}):
                    category_info_id = get_response(y)
                    print(status)
                category_info = discord.Guild.get_channel(ctx.guild, int(category_info_id))
            except Exception as e:
                print(f"Error in fetching category: {e} ")
            if category_info is None:
                category_info = await ctx.guild.create_category(name="↢↢↢↢↢『DailyDose』↣↣↣↣↣", position=0)
            history_channel = await ctx.guild.create_text_channel(name=f"『🤔』: Daily-History",
                                                                  overwrites=overwrites_text_channel,
                                                                  category=category_info, news=True)
            find_server = {"guild id": ctx.guild.id}
            enable_stats = {"$set": {"daily history status": True, "history channel id": history_channel.id,
                                     "category info id": category_info.id}}
            if find_server is not None:
                server_collection.update_one(find_server, enable_stats)
                await ctx.reply(f"Successfully enabled daily history")
        else:
            await ctx.reply(f"Daily history is already enabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="history disable", aliases=("dh",), help="Disables daily history")
    async def history_disable(self, ctx):
        global find, status, history_channel_id, quote_channel_id, category_info_id
        for y in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "daily history status": 1}):
            status = get_response(y)

        if status == "True":
            for x in server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "category info id": 1}):
                category_info_id = get_response(x)
                find = x
            try:
                for history_channel in server_collection.find({"guild id": ctx.guild.id},
                                                              {"_id": 0, "history channel id": 1}):
                    history_channel_id = get_response(history_channel)
            except Exception as e:
                print(f"Error occurred: {e}")
                history_channel_id = None

            try:
                for quote_channel in server_collection.find({"guild id": ctx.guild.id},
                                                            {"_id": 0, "quote channel id": 1}):
                    quote_channel_id = get_response(quote_channel)
            except Exception as e:
                print(f"Error occurred: {e}")
                quote_channel_id = None
            try:
                info_category = discord.Guild.get_channel(ctx.guild, int(category_info_id))
                if quote_channel_id is not None:
                    quote_channel = discord.Guild.get_channel(ctx.guild, int(quote_channel_id))
                if history_channel_id is not None:
                    history_channel = discord.Guild.get_channel(ctx.guild, int(history_channel_id))
                if info_category is not None:
                    for channel in info_category.text_channels:
                        if channel == history_channel:
                            await channel.delete()

                if quote_channel is None:
                    await info_category.delete()
                    category_info_id = 0

            except Exception as e:
                await ctx.reply(f"Error Occurred: {e}")

            disable_stats = {"$set": {"daily history status": False, "history channel id": 0,
                                      "category info id": int(category_info_id)}}
            find_server = {"guild id": ctx.guild.id}
            if find_server is not None:
                server_collection.update_one(find_server, disable_stats)
                await ctx.reply(f"Successfully disabled daily history")
        else:
            await ctx.reply(f"Daily history is already disabled")

    @commands.has_permissions(administrator=True)
    @commands.command(name="change_prefix", aliases=("cp",), help="Changes the prefix for server")
    async def change_prefix(self, ctx, prefix):
        find_server = {"guild id": ctx.guild.id}
        set_prefix = {"$set": {"command prefix": f"{prefix}"}}
        if find_server is not None:
            server_collection.update_one(find_server, set_prefix)
        await ctx.reply(f"Successfully changed prefix to ```{prefix}```")

    @commands.has_permissions(administrator=True)
    @commands.command(name="change_prefix", aliases=("cp",), help="Changes the prefix for server")
    async def add_new_channel(self, ctx, name, category_id):
        category = ctx.guild.get_channel(category_id)
        created_channel = await ctx.guild.create_voice_channel(name=f"{name}", category=category)

    # @commands.command(name="change date channel", aliases=("cdatec",),
    #                   help="Changes bot date Channel for this server : copy id of channel and paste after command")
    # @commands.has_permissions(administrator=True)
    # async def change_date_channel(self, ctx, date_channel_id):
    #     find_server = {"guild id": ctx.guild.id}
    #     set_date_channel = {"$set": {"date channel": int(date_channel_id)}}
    #     if find_server is not None:
    #         server_collection.update_one(find_server, set_date_channel)
    #         await ctx.reply(f"Quote Channel Changed to {date_channel_id}")
    #
    # @commands.command(name="change day channel", aliases=("cdayc",),
    #                   help="Changes bot Time Channel for this server : copy id of channel and paste after command")
    # @commands.has_permissions(administrator=True)
    # async def change_day_channel(self, ctx, day_channel_id):
    #     find_server = {"guild id": ctx.guild.id}
    #     set_day_channel = {"$set": {"day channel": int(day_channel_id)}}
    #     if find_server is not None:
    #         server_collection.update_one(find_server, set_day_channel)
    #         await ctx.reply(f"Day Channel Changed to {day_channel_id}")
    #
    # @commands.command(name="change history channel", aliases=("chc",),
    #                   help="Changes History Channel for this server : copy id of channel and paste after command")
    # @commands.has_permissions(administrator=True)
    # async def change_history_channel(self, ctx, history_channel_id):
    #     find_server = {"guild id": ctx.guild.id}
    #     set_history_channel = {"$set": {"history channel": int(history_channel_id)}}
    #     if find_server is not None:
    #         server_collection.update_one(find_server, set_history_channel)
    #         await ctx.reply(f"History Channel Changed to {history_channel_id}")
    #
    # @commands.command(name="change quote channel", aliases=("cqc",),
    #                   help="Changes Quote Channel for this server : copy id of channel and paste after command")
    # @commands.has_permissions(administrator=True)
    # async def change_quote_channel(self, ctx, quote_channel_id):
    #     find_server = {"guild id": ctx.guild.id}
    #     set_quote_channel = {"$set": {"quote channel": int(quote_channel_id)}}
    #     if find_server is not None:
    #         server_collection.update_one(find_server, set_quote_channel)
    #         await ctx.reply(f"Quote Channel Changed to {quote_channel_id}")


def setup(bot):
    bot.add_cog(Management(bot))
