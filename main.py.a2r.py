# music cog nem lesz automatikusan hozzáadva
import datetime
import random
import asyncio
import discord
from discord.ext import commands

TOKEN = 'token'  # git verzió miatt a tokent kitöröltem, futáshoz meg kell adni a Discord Dev oldalon található tokent
description = 'Szédületes bot in Python'
bot = commands.Bot(command_prefix='?', description=description)
new_Version = False
major_version_change = False
# a main mappáján belül kell egy mappának lennie, ami a cogokat tartalmazza, ezt előtagként hozzá kell illeszteni
extensions = [
    'cogs.adminonly',
    'cogs.events',
    'cogs.commands',
    'cogs.balaton',
    'cogs.experimental',
    'cogs.musicSajat'
]


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='commands || ?help'))
    if new_Version:
        await bot.get_channel(549709362206081076).send(":loudspeaker: @here Hey, I've just been updated!" +
            " Type '?changelog' to see what's :new:! ")
    if major_version_change:
        await bot.get_channel(399595938013773824).send(":loudspeaker: Hey everyone!" +
            "\nI'm making my way out of alpha! This means most of the bugs have been fixed, " +
                "but you might still experience some issues. If you discover any bugs, please " +
                "report them by using the ``?bug`` command." +
            "\nIf you need help with the commands, please type ``?help``." +
            "\nType ``?changelog`` to see what's new"
        )
    await bot.get_channel(549709362206081076).send("I'm back online! :globe_with_meridians: :white_check_mark:")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()


@bot.command(aliases=['uotime', 'ut', 'upt'])
async def uptime(ctx):
    elso = True
    await ctx.message.delete()
    while True:
        try:
            uptime = str(get_bot_uptime())
            uptime_split_array = uptime.split()
            # a parancs lefutásakor (?ut) kiírjuk a channelbe is az uptimeot, viszont utána óránként már nem
            if elso:
                await ctx.send(f'Uptime: **{uptime}**')
                elso = False
            # 0 hours, 0 minutes, and 5 seconds
            # 0   1    2    3      4  5    6
            # 17 days, 19 hours, 59 minutes, and 44 seconds
            # 0     1   2   3     4     5     6   7     8

            if len(uptime_split_array) < 8:
                napok_masodpercben = 0
                orak_masodpercben = int(uptime_split_array[0]) * 3600
                percek_masodpercben = int(uptime_split_array[2]) * 60
                masodpercek = int(uptime_split_array[5])
            else:
                napok_masodpercben = int(uptime_split_array[0]) * 24 * 3600
                orak_masodpercben = int(uptime_split_array[2]) * 3600
                percek_masodpercben = int(uptime_split_array[4]) * 60
                masodpercek = int(uptime_split_array[7])

            # if len(uptime_split_array) > 7:
            #     napok_masodpercben = uptime_split_array[0] * 24 * 3600
            #     orak_masodpercben = uptime_split_array[2] * 3600
            #     percek_masodpercben = uptime_split_array[4] * 60
            #     masodpercek = uptime_split_array[8]
            # else:
            #     napok_masodpercben = 0
            #     orak_masodpercben = uptime_split_array[0] * 3600
            #     percek_masodpercben = uptime_split_array[2] * 60
            #     masodpercek = uptime_split_array[5]

            # napok_masodpercben = uptime_split_array[0] * 24 * 3600
            # orak_masodpercben = uptime_split_array[2] * 3600
            # percek_masodpercben = uptime_split_array[4] * 60
            # masodpercek = uptime_split_array[7]
            osszesen_masodpercben = napok_masodpercben + orak_masodpercben + percek_masodpercben + masodpercek
            try:
                file = open("/srv/shared/Simi/programozas/discordbot/0rekord.txt", "r")
                fajlban_tarolt = int(file.readline())
                file.close()
            # except FileNotFoundError:
            except IOError:
                file = open("/srv/shared/Simi/programozas/discordbot/0rekord.txt", "w")
                file.write(f'{osszesen_masodpercben}\n{uptime}')
                file.close()
                fajlban_tarolt = 1
            if osszesen_masodpercben > fajlban_tarolt:
                file = open("/srv/shared/Simi/programozas/discordbot/0rekord.txt", "w")
                file.write(f'{osszesen_masodpercben}\n{uptime}')
                file.close()
        except Exception as error:
            await ctx.send(f"Error while accessing file '0rekord.txt': {error}")
        await asyncio.sleep(3600)
    # await ctx.send('Uptime: **{}**'.format(get_bot_uptime()))
    # await ctx.send(f'Uptime: **{uptime}**')

def get_bot_uptime():
    return get_human_readable_uptime_diff(bot.uptime)

def get_human_readable_uptime_diff(start_time):
    now = datetime.datetime.utcnow()
    delta = now - start_time
    (hours, remainder) = divmod(int(delta.total_seconds()), 3600)
    (minutes, seconds) = divmod(remainder, 60)
    (days, hours) = divmod(hours, 24)
    if days:
        fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
    else:
        fmt = '{h} hours, {m} minutes, and {s} seconds'
    return fmt.format(d=days, h=hours, m=minutes, s=seconds)


@bot.command(aliases=['l'])
async def load(ctx, extension):
    'Admin-only command.'
    if ctx.author.id == 358992693453652000:
        try:
            bot.load_extension(extension)
            await ctx.message.delete()
            await ctx.send('Loaded {} :white_check_mark: '.format(extension), delete_after = 5)
        except Exception as error:
            await ctx.send("{} can't be loaded. [{}]".format(extension, error))
    else:
        await ctx.send('You cannot do that. :no_entry:')


@bot.command(aliases=['uload', 'ul'])
async def unload(ctx, extension):
    'Admin-only command.'
    if ctx.author.id == 358992693453652000:
        try:
            await ctx.message.delete()
            bot.unload_extension(extension)
            await ctx.send(f'Unloaded {extension} :white_check_mark: ', delete_after=5)
        except Exception as error:
            await ctx.send("{} can't be unloaded. [{}]".format(extension, error))
    else:
        await ctx.send('You cannot do that. :no_entry:')

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
bot.run(TOKEN)