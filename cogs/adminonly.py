import datetime
import discord
from discord.ext import commands

class AdminOnly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx):
        "Changes the bot's status. Syntax: ?status type[str] status-to-show[str]" #play listen
        if ctx.message.author.id == 358992693453652000:
            if len(ctx.message.content) == 7:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='commands || ?help'))
                message = 'Status updated. :white_check_mark:'
                await ctx.send('{}'.format(message))
            elif len(ctx.message.content) >= 8:
                if "play" in ctx.message.content:
                    try:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=ctx.message.content[13:]))
                        message = 'Status updated. :white_check_mark:'
                        await ctx.send('{}'.format(message))
                    except Exception:
                        await ctx.send("Status change failed. :x: ")
                elif "listen" in ctx.message.content:
                    try:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=ctx.message.content[15:]))
                        message = 'Status updated. :white_check_mark:'
                        await ctx.send('{}'.format(message))
                    except Exception:
                        await ctx.send("Status change failed. :x: ")
                elif "watch" in ctx.message.content:
                    try:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=ctx.message.content[14:]))
                        message = 'Status updated. :white_check_mark:'
                        await ctx.send('{}'.format(message))
                    except Exception:
                        await ctx.send("Status change failed. :x: ")
                elif "stream" in ctx.message.content:
                    try:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=ctx.message.content[15:]))
                        message = 'Status updated. :white_check_mark:'
                        await ctx.send('{}'.format(message))
                    except Exception:
                        await ctx.send("Status change failed. :x: ")
                else:
                    await ctx.send("Wrong syntax.")
            else:
                await ctx.send('Error')
        else:
            await ctx.send("You don't have permission(s) to do that. :no_entry:")

    @commands.command()
    async def say(self, ctx):
        'Sends a message. Syntax: ?say channelID message_content'
        if ctx.message.author.id == 358992693453652000:
            content = ctx.message.content.split()
            try:
                channel = int(content[1])
            except Exception:
                await ctx.say("Error: Cannot convert str to int.")
            content_word_count = len(content)
            meddig = content_word_count
            kiirando_uzenet = ' ' + content[2]
            for x in range(3, meddig):
                kiirando_uzenet += ' ' + content[x]
            await self.bot.get_channel(channel).send('{}'.format(kiirando_uzenet))
        else:
            await ctx.send('This is an admin-only command.')
    
    #version info
    @commands.command()
    async def version(self, ctx):
        """Prints the current discord.py version. Admin-only."""
        if ctx.message.author.id == 358992693453652000:
            await ctx.send("Discord.py version info: {} ({})".format(discord.__version__, discord.version_info[3]))
        else:
            await ctx.send("Access forbidden :no_entry:")

def setup(bot):
    bot.add_cog(AdminOnly(bot))