import random
import math
import datetime
import asyncio
import discord
from discord.ext import commands
from cogs.adminonly import is_admin


class Experimental(commands.Cog, name="Experimental"):

    def __init__(self, bot):
        self.bot = bot

    # TODO: is this needed when we have on_command_error?
    @commands.Cog.listener()
    async def on_error(self, event):
        now = datetime.datetime.now()
        try:
            embed = discord.Embed(
                title=f"``{now}:``",
                description=f":interrobang: Non-command error: {event} raised an exception:",
                colour=discord.Colour.from_rgb(255, 0, 13)
            )
            embed.set_thumbnail(url=f"{event.guild.icon.url}")  # TODO: does this return the guild icon?
            embed.set_author(name="Non-command error", icon_url=f"{event.guild.icon.url}")  # TODO: itt is
            await self.bot.get_channel(550724640469942285).send(embed=embed)
        except Exception as e:
            print(f"Non-command error. Couldn't send an error message to the logs channel. ({e})")

    @commands.group(name="Emojis", aliases=["e", "emote", "emotes", "emojis", "emoji"], case_insensitive=True)
    async def emoji(self, ctx):
        """A command group for custom ascii emojis."""

    @emoji.command(aliases=["s"])
    async def shrug(self, ctx):
        await ctx.message.delete()
        await ctx.send("¯\\_(ツ)_/¯")

    @emoji.command(aliases=["tf"])
    async def tableflip(self, ctx):
        await ctx.message.delete()
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @emoji.command(aliases=["uf"])
    async def unflip(self, ctx):
        await ctx.message.delete()
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    @emoji.command(aliases=["lf", "lennyface"])
    async def lenny(self, ctx):
        await ctx.message.delete()
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @emoji.command(aliases=["want-a-taco", "taco", "t"])
    async def wat(self, ctx):
        await ctx.message.delete()
        await ctx.send("{\\\_\/}\n(●\_●)\n( >🌮 Want a taco?")

    # TODO: this command should be revised
    @commands.command(aliases=["remind"])
    async def reminder(self, ctx, time, title):
        """Admin-only. Sets a reminder. Syntax: ?remind time[int, in seconds] title[str, between ""]"""
        if ctx.author.is_owner:
            try:
                time = int(time)
                title = str(title)
                # emoji https://www.fileformat.info/info/unicode/char/2705/index.htm
                await ctx.message.add_reaction(u"\u2705")
                await asyncio.sleep(time)
                await ctx.send(f"{ctx.guild.owner.mention} you wanted me to remind you to {title}")
            except Exception as e:
                await ctx.send(f"Error creating reminder. ({e})")
        else:
            await ctx.send("This command is admin-only.")

    # tesztelésre vár + képeket be kell szerezni
    @commands.command(aliases=["Kóka", "kóka"])
    async def koka(self, ctx):
        """Best command to date."""
        rnd = random.randint(1, 4)
        kep = discord.File(fp=f"../resources/images/koka{rnd}.jpg")
        await ctx.message.delete()
        await ctx.send(file=kep)

    # THIS FUNCTION IS YET TO BE TESTED!
    # gyakorlatilag mehet commands.py-ba
    @commands.command(aliases=["edit", "limit", "max"])  # max user egy voice channelben
    async def changelimit(self, ctx, limit: int, time_length: float = 120, *args):
        """
            Az 'Itt-nem-zavar-a-Szédületes' channelt lehet kisajátítani adott időre.
            Syntax: ?max [limit(int)] *[ido_percben(float)=120] *[args]

            PARAMETERS
            ----------
            ctx: discord.ext.commands.Context
                The context in which the command was invoked; gets passed automatically
            limit: int
                The number of max users allowed in the voice channel
            time_length: float
                The number of minutes until the limit will reset to unlimited, default is 120
            args:
                The cause of reservation
        """
        now = datetime.datetime.now()
        try:
            file = open("/srv/shared/Simi/programozas/discordbot/0foglalas.txt", "r")
            is_reserved = bool(file.readline() == "True")  # this will be a string, not bool
            if is_reserved:  # if True, the channel cannot be reserved
                file.close()
                raise commands.CommandError("A szobát már lefoglalták.")
            else:  # if False, the channel will be reserved
                # the file should contain True as is_reserved will get this value
                file.write("True")
                file.close()
        except OSError:  # if file is not found
            file = open("/srv/shared/Simi/programozas/discordbot/0foglalas.txt", "w")
            file.write("True")  # if this command is called, is_reserved should be set to True
            file.close()

        if time_length > 4500:  # Max allowed reservation length is 27000 seconds = 4500 minutes = 7.5 hours
            raise commands.BadArgument("Maximum 4500 percre (7,5 óra) foglalhatod a szobát.")
        elif time_length - 9 < 1:  # A warning message is sent 5 minutes before the end of the reservation
            raise commands.BadArgument("Minimum 10 percre kell foglalnod.")

        time_length = math.ceil(time_length * 60)  # converting minutes to seconds
        requester = ctx.author
        guild = ctx.message.guild
        channel_to_edit = discord.utils.get(guild.voice_channels, name="Itt-nem-zavar-a-Szédületes")
        minimum_role = discord.utils.get(ctx.guild.roles, name="Balaton Squad")
        top_role = requester.top_role
        await ctx.message.delete()

        if top_role >= minimum_role:
            if (limit > 0) and (limit < 99):
                await channel_to_edit.edit(user_limit=limit)
                await ctx.send(f"User limit has been updated to {limit}. It will be set to unlimited in "
                               f"{round((time_length / 60), 2)} minutes.", delete_after=30)
                # --- EMBED WITH INFO ABOUT THE RESERVATION ---
                # only if args is not none
                if args:
                    reservation_ends = now + datetime.timedelta(0, time_length)
                    embed = discord.Embed(
                        title=f"Foglalás részletei:",
                        colour=discord.Colour.orange()
                    )
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_author(name=f"Szoba lefoglalva", icon_url=ctx.guild.icon_url)
                    embed.set_footer(text=f"{now}")
                    embed.add_field(name="Foglalás oka:", value=f"{' '.join(args)}", inline=False)
                    embed.add_field(name="Foglalta:", value=f"{ctx.author.mention}", inline=True)
                    embed.add_field(name="Létszámkorlát:", value=f"{limit} fő", inline=True)
                    embed.add_field(name="Időtartam:", value=f"{math.ceil(time_length / 60)} perc", inline=True)
                    embed.add_field(name="Foglalás lejár:", value=f"{reservation_ends}", inline=False)
                    await self.bot.get_channel(484010396076998686).send(embed=embed)
                # --- THIS EMBED IS SENT TO #LOGS ---
                embed = discord.Embed(
                    title=f"``{now}:``",
                    description=f"{ctx.author.mention} has changed the user limit of {channel_to_edit.mention} "
                                f"to {limit} for {round((time_length / 60), 2)} minutes.",
                    colour=discord.Colour.magenta()
                )
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_author(name="Voice channel user limit updated", icon_url=ctx.author.avatar_url)
                await self.bot.get_channel(550724640469942285).send(embed=embed)  # this goes to #logs
                # --- END OF EMBED ---

                await asyncio.sleep(time_length - 300)  # sleeps for the given length of time minus 5 minutes
                await ctx.send("User limit will be set to unlimited in 5 minutes.", delete_after=120)
                await asyncio.sleep(300)  # A warning message is sent 5 minutes before the end of the reservation
                await channel_to_edit.edit(user_limit=0)
                file = open("/srv/shared/Simi/programozas/discordbot/0foglalas.txt", "w")
                file.write("False")  # reservation period ended, the channel can be reserved again
                file.close()
                await ctx.send("User limit has been set to unlimited.", delete_after=10)
            elif (limit < 0) or (limit > 99):
                raise commands.BadArgument("Limit must be between 1 and 99.")
            elif limit == 0:
                await channel_to_edit.edit(user_limit=limit)
                embed = discord.Embed(
                    title=f"``{now}:``",
                    description=f"{ctx.author.name} has set the user limit of {channel_to_edit.mention} to unlimited",
                    colour=discord.Colour.magenta()
                )
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_author(name="Voice channel user limit updated", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await asyncio.sleep(1)
                await self.bot.get_channel(550724640469942285).send(embed=embed)
        else:
            raise commands.CheckFailure("You aren't allowed to change the channel's settings.")

    # gyakorlatilag mehet commands.py-ba
    @commands.command()
    async def ping(self, ctx):
        """Checks the bot's latency."""
        now = datetime.datetime.now()
        guild = ctx.message.guild
        embed = discord.Embed(
            title=f"``{now}:`` ",
            description=f"Current ping to *{guild.name}* is {round((self.bot.latency * 1000), 2)} ms",
            colour=discord.Colour.blurple()
        )
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name="Pong!", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f"This message was requested by {ctx.author.name}")
        await ctx.message.delete()
        await ctx.send(embed=embed)

    # sub role automatikus hozzáadása
    @commands.command(hidden=True)
    async def sub(self, ctx):
        sub_role = discord.utils.get(ctx.guild.roles, name="sub")
        member = ctx.author
        await member.add_roles(sub_role)
        await ctx.message.delete()
        await self.bot.get_channel(549709362206081076).send("<@358992693453652000> "
                                                            f"sub role has been assigned to {member.name}.")
        await ctx.send(f"Hey {member.mention}, access granted!")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def delay_message(self, ctx, channel: discord.TextChannel, delay: int, *args):
        """Sends your message to a given channel after the given amount of seconds."""
        await ctx.message.delete()
        when = datetime.datetime.now() + datetime.timedelta(0, delay)
        await ctx.send(f"Your message will be sent in {delay} seconds ({when}, channel: {channel.mention})",
                       delete_after=15)
        await asyncio.sleep(delay)
        await channel.send(" ".join(args))


def setup(bot):
    bot.add_cog(Experimental(bot))
