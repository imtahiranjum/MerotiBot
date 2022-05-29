from Functions.database import server_collection, get_response
from pytz import timezone
from _datetime import datetime


# current_area_time = time_get("Asia/Karachi")
# time_now = current_area_time.strftime("%H:%M")


# async def auto_quote(bot):
#     for x in server_collection.find({"quote status": "true"}, {"_id": 0, "quote channel": 1}):
#         try:
#             channel = bot.get_channel(int(get_response(x)))
#             print(channel)
#             try:
#                 await channel. \
#                     send(f'Quote of the Day\n@daily_quotes\n',
#                          embed=microsoft_translator_quote_ur("none", random.choice(sequence)))
#             except KeyError:
#                 print("Channel Not Set!")
#         except Exception as e:
#             print(f"Error occurred: {e}")
#
#
# async def auto_history(bot):
#     for x in server_collection.find({}, {"_id": 0, "history channel": 1}):
#         try:
#             channel = bot.get_channel(int(get_response(x)))
#             print(channel)
#             if channel != "None":
#                 try:
#                     await channel. \
#                         send(f'@daily_history\n'
#                              ,
#                              embed=history_today_second("none"))
#                 except KeyError:
#                     print("Channel Not set!")
#         except Exception as e:
#             print(f"Error occurred: {e}")
#
#
# async def auto_day(bot):
#     current_area_time = time_get("Asia/Karachi")
#     day_for_automation = current_area_time.strftime("%A")
#     for x in server_collection.find({}, {"_id": 0, "day channel": 1}):
#         if x is not None:
#             try:
#                 channel = bot.get_channel(int(get_response(x)))
#                 if channel != "None":
#                     try:
#                         await channel.edit(name=f"『📅』: {day_for_automation}")
#                     except KeyError:
#                         print("Channel Not Set")
#             except Exception as e:
#                 print(f"Error occurred: {e}")
#
#
# async def auto_date(bot):
#     current_area_time = time_get("Asia/Karachi")
#     date_for_automation = current_area_time.strftime("%d-%b-%Y")
#     for x in server_collection.find({}, {"_id": 0, "date channel": 1}):
#         try:
#             channel = bot.get_channel(int(get_response(x)))
#             if channel != "None":
#                 try:
#                     await channel.edit(name=f"『📆』: {date_for_automation}")
#                 except KeyError:
#                     print("Channel Not Set")
#         except Exception as e:
#             print(f"Error occurred: {e}")


def time_get(area):
    timeArea = timezone(f'{area}')
    date_and_time = datetime.now(timeArea)
    return date_and_time


async def database_creation(ctx):
    info = {"guild name": ctx.name,
            "guild id": ctx.id,
            "date channel id": 0,
            "day channel id": 0,
            "history channel id": 0,
            "quote channel id": 0,
            "members channel id": 0,
            "bots channel id": 0,
            "category info id": 0,
            "category day and date id": 0,
            "category stats id": 0,
            "stats status": False,
            "time and date status": False,
            "daily quotes status": False,
            "quotes type": "nil",
            "daily history status": False,
            "command prefix": "m"}

    server_collection.insert_one(info)


async def database_deletion(ctx):
    server_collection.delete_many({"guild id": ctx.id})


async def stats_update(ctx, bot):
    guild = ctx.guild
    total_members = guild.member_count
    for_all_person = server_collection.find({"guild id": guild.id, "stats status": "true"},
                                            {"_id": 0, "members channel id": 1})
    print(for_all_person)
    for x in for_all_person:
        try:
            channel = bot.get_channel(int(get_response(x)))
            try:
                await channel.edit(name=f"『🤵』 Members: {total_members}")
                print("Updated Counter")
            except Exception as e:
                print(f"Channel Not Set: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")

    bot_counter = 0
    try:
        for x in ctx.guild.members:
            if x.bot:
                bot_counter = bot_counter + 1
    except Exception as e:
        print(f"Couldn't count bots because following error occurred:- \n{e}")

    for_bots = server_collection.find({"guild id": ctx.guild.id}, {"_id": 0, "bots channel id": 1})
    for x in for_bots:
        try:
            channel = bot.get_channel(int(get_response(x)))
            try:
                await channel.edit(name=f"『🤖』 Bots: {bot_counter}")
                print("Updated Counter")
            except Exception as e:
                print(f"Channel Not Set: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")
