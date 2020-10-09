import discord
from discord.ext import commands
import platform


async def is_admin(ctx):
    """Checks whether the user who called an admin-only command has rights to run these commands"""
    admins = [358992693453652000]  # the Discord IDs of people who may run Admin-only commands
    return ctx.author.id in admins


async def is_moderator(ctx):
    """Checks if user is DAM :)"""
    # DAM, Simi
    ids = [162662873980469257, 358992693453652000]
    return ctx.author.id in ids


class AdminOnly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_admin)
    async def status(self, ctx, *args):
        """Changes the bot's status. Syntax: ?status type[str] status-to-show[str]"""  # play listen
        if not args:
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.listening, name="commands || ?help"))
        else:
            activity = args[0]
            args = args[1:]  # cut the activity's name from the tuple
            name = " ".join(args)
            if activity == "play":
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=name))
            elif activity == "listen":
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening, name=name))
            elif activity == "watch":
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
            elif activity == "stream":
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.streaming, name=name))
            else:
                await ctx.send("Wrong syntax. See ``?help status`` for details.")
                return  # don't send the success message
        await ctx.send("Status updated. :white_check_mark:")

    @commands.command(aliases=["send"])
    @commands.check(is_moderator)
    async def say(self, ctx, channel: discord.TextChannel, *args):  # ctx is needed even if its not used
        """Sends a message. Syntax: ?say channel_mention message_content"""
        if not args:
            raise commands.BadArgument("Nem küldhetsz üres üzenetet.")
        await self.bot.get_channel(channel.id).send(f"{' '.join(args)}")

    @commands.command(aliases=["v"])
    @commands.check(is_admin)
    async def version(self, ctx):
        """Prints the current discord.py version. Admin-only."""
        await ctx.send(f"Discord.py version {discord.__version__} running on {platform.system()}")

    @commands.command()
    @commands.check(is_admin)
    async def close(self, ctx):
        await ctx.send(":sleeping:")
        await self.bot.close()


def setup(bot):
    bot.add_cog(AdminOnly(bot))
