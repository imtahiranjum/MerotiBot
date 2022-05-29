import os
import discord
from discord.ext import commands, tasks
import datetime
import random
import asyncio
from ping import keep_alive
from Functions.database import server_collection, get_response
from Functions.management import database_creation, stats_update, time_get

intents = discord.Intents.all()
mentions = discord.AllowedMentions.all()


def get_prefix(guild_bot, message):
    global check
    check = False
    for x in server_collection.find({"guild id": message.guild.id}, {"_id": 0, "command prefix": 1}):
        check = True
        print(f"Being Called in {message.guild.name}")
        print(f"Message: {message.content} \n"
              f"Channel: {message.channel.name}")
        if x is None:
            return "m"
        else:
            print(get_response(x))
            return str(get_response(x))
    else:
        pass


bot = commands.Bot(command_prefix=get_prefix, intents=intents)

for cogs in os.listdir("./Commands"):
    if cogs.endswith(".py"):
        bot.load_extension(f"Commands.{cogs[:-3]}")


@bot.event
async def on_guild_join(ctx):
    embed = discord.Embed(title="Hi! I am Meroti, your friend and assistant!",
                          timestamp=datetime.datetime.utcnow(), color=0xdb0000)
    thumbnail_icon = ctx.icon
    if thumbnail_icon is not None:
        embed.set_thumbnail(url=str(ctx.icon))
    embed.add_field(name="My Intro", value="I am a multi purpose bot with many functions and features like "
                                           "moderation, utilities, management and more.", inline=True)
    embed.add_field(name="My Usage", value="My prefix is ```m```, you can change it by using ```m cp``` "
                                           "Use ```m help``` to see the commands.", inline=True)
    embed.set_footer(text="Thank You for adding me in your server!")
    channel = ctx.system_channel
    if channel is not None:
        await channel.send(embed=embed)
    else:
        channel = ctx.public_updates_channel
        if channel is not None:
            await channel.send(embed=embed)
        else:
            print("No channels set!")
    await database_creation(ctx)


@bot.event
async def on_member_join(ctx):
    await stats_update(ctx, bot)


@bot.event
async def on_member_remove(ctx):
    await stats_update(ctx, bot)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="just booted!"))
    print("Logged in!")
    auto_tasks.start()
    # auto_tasks_2.start()


@tasks.loop(seconds=360.0)
async def auto_tasks():
    statuses = ["with you!", "without you!",  "with Crypto!", "with humans!", "with Hearts!", "with Toys!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


# @tasks.loop(seconds=59.0)
# async def auto_tasks_2():
#     print(current_area_time.strftime("%H:%M\n %a, %d-%b-%Y"))
#     if time_now == scheduled_time[0]:
#         await auto_quote(bot)
#     if time_now == scheduled_time[1]:
#         await auto_history(bot)
#     if time_now == scheduled_time[2]:
#         await auto_day(bot)
#         await auto_date(bot)


try:
    keep_alive()
except ConnectionError:
    print("Not hosted on rt or something else")

bot_auth_token = f"{os.environ['bot_auth_token']}"
bot.run(bot_auth_token)
