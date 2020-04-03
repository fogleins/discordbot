import random
import math  # used in function 'changelimit'
import datetime
import asyncio
import discord
from discord.ext import commands


class Experimental(commands.Cog, name="Experimental"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event):
        now = datetime.datetime.now()
        try:
            embed = discord.Embed(
                title=f"``{now}:``",
                description=f":interrobang: Non-command error: {event} raised an exception:",
                colour=discord.Colour.from_rgb(255, 0, 13)
            )
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/URc4P573HFyaYe6vysVJ5GDeG4yf675sa"
                                    "-vT9IjYMao/%\3Fsize%3D1024/https/cdn.discordapp.com/icons/399595937409925140"
                                    "/b80c7368fbb679d750c7c0809295a555.webp")
            embed.set_author(name="Non-command error", icon_url="https://emojipedia-us.s3.dualstack.us-west-1"
                                                                ".amazonaws.com/thumbs/120/twitter/185/cross"
                                                                "-mark_274c.png")
            await self.bot.get_channel(550724640469942285).send(embed=embed)
        except Exception as e:
            print(f"Non-command error. Couldn't send an error message to the logs channel. ({e})")

    @commands.group(name="Emojis", aliases=["e", "emote", "emotes"])
    async def emoji(self, ctx):
        await ctx.send("A command group for custom ascii emojis.")

    @emoji.command(aliases=["s"])
    async def shrug(self, ctx):
        await ctx.message.delete()
        await ctx.send("¯\\_(ツ)_/¯")

    @emoji.command(aliases=["tf"])
    async def tableflip(self, ctx):
        await ctx.message.delete()
        await ctx.send("\\tableflip")

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

    # TODO: nem kell
    @commands.command(hidden=True)
    # ahhoz, hogy más szerveren lévő user egyes adatait (pl. 
    # a jelenlegi voice channel nevét, a szerver nevét megkapjuk
    # member helyett user-ként kellene kezelni, de ezeknek nincsenek
    # ilyen attribútumai (pl. user.status, user.voice), így ennek a 
    # parancsnak nem igazán van így értelme)
    # async def tesztusrinfo(self, ctx, member: discord.User): #ez így nem működik
    # helyes megoldás lenne:
    async def tesztusrinfo(self, ctx, member: discord.Member):
        try:
            await ctx.send(f"Name: {member.name}; Status: {member.status}; "
                           f"Connected to: {member.voice.channel.name} on {member.voice.channel.guild.name}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    # tesztelésre vár + képeket be kell szerezni
    @commands.command(aliases=["Kóka", "kóka"])
    async def koka(self, ctx):
        """Best command to date."""
        rnd = random.randint(1, 4)
        kep = discord.File(fp=f"/srv/shared/Simi/programozas/discordbot/rwLive/cogs/koka{rnd}.jpg")
        await ctx.message.delete()
        await ctx.send(file=kep)

    # TODO: nem kell
    @commands.command()
    async def playthis(self, ctx, *, url):
        """Plays your most played songs/playlists. (Under testing, might be buggy)"""
        message = ctx.message
        teljes_uzenet_splitelve = ctx.message.content.split()
        link = teljes_uzenet_splitelve[len(teljes_uzenet_splitelve) - 1]
        music_bot_channel_id = 443844561270341633
        await self.bot.get_channel(music_bot_channel_id).send(f"!play {link}")
        await message.delete()

    # TODO: nem kell
    # ugyanaz, mint a spotiplay-nél
    @commands.command(aliases=["kutyafül"])
    async def kokalista(self, ctx):
        """Kóka úr kedvelt YT videóit tartalmazó playlistet kezdi lejátszani"""
        lista_url = "https://www.youtube.com/playlist?list=LLaPUXOjl02GaQKAtRi1KnxQ"
        message = ctx.message
        await self.bot.get_channel(443844561270341633).send(f"!play {lista_url}")
        await message.delete()

    # THIS FUNCTION IS YET TO BE TESTED!
    # gyakorlatilag mehet commands.py-ba
    @commands.command(aliases=["edit", "limit", "max"])  # max user egy voice channelben
    async def changelimit(self, ctx, limit: int, time_length: float = 120):
        """
            Az 'Itt-nem-zavar-a-Szédületes' channelt lehet kisajátítani adott időre.
            Syntax: ?max [limit(int)] *[ido_percben(float)=120]
        """
        """
            PARAMETERS
            ----------
            limit: int
                The number of max users allowed in the voice channel
            time_interval: float
                The number of minutes until the limit will reset to unlimited, default is 120
        """
        try:
            now = datetime.datetime.now()
            if time_length is None:
                time_length = 120  # zh-k miatt inkább 2 órára lett növelve
            elif time_length > 4500:  # Max allowed reservation length is 27000 seconds = 4500 minutes = 7.5 hours
                await ctx.send(":x: Maximum 4500 percre (7,5 óra) foglalhatod a szobát.")
                return
            elif time_length - 9 < 1:  # A warning message is sent 5 minutes before the end of the reservation
                await ctx.send(":x: Minimum 10 percre kell foglalnod.")
                return

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
                                   f"{time_length / 60} minutes.", delete_after=30)
                    # --- EMBED IS BEING SENT TO #LOGS ---
                    embed = discord.Embed(
                        title=f"``{now}:``",
                        description=f"{ctx.author.mention} has changed the user limit of {channel_to_edit.mention} "
                                    f"to {limit} for {time_length} minutes.",
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
                    await ctx.send("User limit has been set to unlimited.", delete_after=10)
                elif (limit < 0) or (limit > 99):
                    await ctx.send(":x: Limit must be between 1 and 99.", delete_after=30)
                    return
                elif limit == 0:
                    await channel_to_edit.edit(user_limit=limit)
                    embed = discord.Embed(
                        title=f"``{now}:``",
                        description=f"{ctx.author.name} has set the user limit of {channel_to_edit.mention} "
                                    "to unlimited",
                        colour=discord.Colour.magenta()
                    )
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_author(name="Voice channel user limit updated", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    await asyncio.sleep(1)
                    await self.bot.get_channel(550724640469942285).send(embed=embed)
            else:
                await ctx.send("You aren't allowed to change the channel's settings.")
        except Exception as e:
            print(f"Error in function 'changelimit'. [{e}]")

    # TODO: nem kell
    # mivel a music botok nem játszák le amit másik bot kér, ezért csak shortcutnak jó
    @commands.command(aliases=["splay"])
    async def spotiplay(self, ctx):
        """Sends a play command with the song to which the requester is currently listening to."""
        try:
            member = ctx.author
            if member.activity:
                if member.activity.name == "Spotify":
                    spotify = member.activity
                    await ctx.send(f"!play {spotify.title} by {spotify.artist}", delete_after=30)
                else:
                    await ctx.send("No Spotify listening activity detected.", delete_after=5)
            else:
                await ctx.send("No Spotify listening activity detected.", delete_after=5)
        except Exception as err:
            await ctx.send(f"Error: {err}")

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
        try:
            sub_role = discord.utils.get(ctx.guild.roles, name="sub")
            member = ctx.author
            await member.add_roles(sub_role)
            await ctx.message.delete()
            await self.bot.get_channel(549709362206081076).send("<@358992693453652000> "
                                                                f"sub role has been assigned to {member.name}.")
            await ctx.send(f"Hey {member.mention}, access granted!")
        except Exception as error:
            await ctx.send(f"Something went wrong. :( ({error})")


def setup(bot):
    bot.add_cog(Experimental(bot))
