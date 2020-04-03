import discord
from discord.ext import commands


async def is_admin(ctx):
    """Checks whether the user who called an admin-only command has rights to run these commands"""
    admins = [358992693453652000]  # the Discord IDs of people who may run Admin-only commands
    return ctx.author.id in admins


class AdminOnly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_admin)
    async def status(self, ctx):
        """Changes the bot's status. Syntax: ?status type[str] status-to-show[str]"""  # play listen
        successful = True
        if len(ctx.message.content) == 7:
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.listening, name="commands || ?help"))
            await ctx.send("Status updated. :white_check_mark:")
        elif len(ctx.message.content) >= 8:
            if "play" in ctx.message.content:
                await self.bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.playing, name=ctx.message.content[13:]))
            elif "listen" in ctx.message.content:
                await self.bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.listening, name=ctx.message.content[15:]))
            elif "watch" in ctx.message.content:
                await self.bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.watching, name=ctx.message.content[14:]))
            elif "stream" in ctx.message.content:
                await self.bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.streaming, name=ctx.message.content[15:]))
            else:
                await ctx.send("Wrong syntax. See ``?help status`` for details.")
                successful = False
            if successful:
                await ctx.send("Status updated. :white_check_mark:")
        else:
            await ctx.send("Wrong syntax. See ``?help status`` for details.")

    # TODO
    @commands.command(aliases=["send"])
    @commands.check(is_admin)
    async def say(self, ctx, channel: discord.TextChannel, *args):  # ctx is needed even if its not used
        """Sends a message. Syntax: ?say channel_mention message_content"""
        await self.bot.get_channel(channel.id).send(f"{' '.join(args)}")
    
    # version info
    @commands.command(aliases=["v"])
    @commands.check(is_admin)
    async def version(self, ctx):
        """Prints the current discord.py version. Admin-only."""
        await ctx.send(f"Discord.py version {discord.__version__} ({discord.version_info[3]})")


def setup(bot):
    bot.add_cog(AdminOnly(bot))
