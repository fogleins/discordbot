import datetime
import discord
from discord.ext import commands

from cogs.database import Database


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.datetime.now()
        role = discord.utils.get(member.guild.roles, name="newcomer")
        await member.add_roles(role)
        uzenet = f"{member.name} ({member.id}) is now part of this discord server!"
        embed = discord.Embed(
            title=f"``{now}:`` ",
            description=f"{uzenet}",
            colour=discord.Colour.magenta()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"{member.name} has joined the server", icon_url=member.avatar_url)
        embed.add_field(name="Hey,", value="<@358992693453652000> you need to see this!")
        await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.datetime.now()
        embed = discord.Embed(
            title=f"``{now}:``",
            description=f"{member.name} ({member.id}) has left this discord server!",
            colour=discord.Colour.dark_magenta()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"{member.name} has just left the server", icon_url=member.avatar_url)
        embed.add_field(name="Hey,", value="<@358992693453652000> you need to see this!")
        await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        now = datetime.datetime.now()
        if (after.author.bot is False) and (before.content != after.content):
            uzenet = (f"The message **{before.content}** has been edited to **{after.content}** "
                      f"by **{after.author.name}** in channel {after.channel.mention}")
            embed = discord.Embed(
                title=f"``{now}:`` ",
                description=f"{uzenet}",
                colour=discord.Colour.orange()
            )
            embed.set_thumbnail(url=after.author.avatar_url)
            embed.set_author(name=f"{after.author.name} has edited a message", icon_url=after.author.avatar_url)
            await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        now = datetime.datetime.now()
        uzenet_content = message.content
        if (message.author.id == 549654750585421825 or uzenet_content.startswith('?')
                or uzenet_content.startswith("Unloaded") or uzenet_content.startswith("Loaded")
                or uzenet_content.startswith("User limit") or len(uzenet_content) > 1000
                or uzenet_content.startswith("\\") or uzenet_content.startswith("/////")):
            pass
        else:
            if message.attachments:
                attachment_link = message.attachments[0].url
                logba_ez_megy = (f"The following message was deleted from {message.channel.mention}: "
                                 f"{attachment_link}")
            else:
                logba_ez_megy = f"The message **{message.content}** was deleted from {message.channel.mention}"
            embed = discord.Embed(
                title=f"``{now}:`` ",
                description=f"{logba_ez_megy}",
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_author(name=f"A message sent by {message.author.name} was deleted",
                             icon_url=message.author.avatar_url)
            await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        now = datetime.datetime.now()
        if not user.bot:
            if reaction.message.attachments:
                attachment_link = reaction.message.attachments[0].url
                kiirando_uzenet = f"{user.name} has added {reaction.emoji} to " \
                                  f"{reaction.message.author}'s message in channel " \
                                  f"{reaction.message.channel.mention}: {attachment_link}"
            else:
                kiirando_uzenet = f"{user.name} has reacted {reaction.emoji} to {reaction.message.author}'s " \
                                  f"message in channel {reaction.message.channel.mention}: {reaction.message.content}"
            embed = discord.Embed(
                title=f"``{now}:``",
                description=f"{kiirando_uzenet}",
                colour=discord.Colour.teal()
            )
            embed.set_thumbnail(url=reaction.message.author.avatar_url)
            embed.set_author(name=f"{user.name} has added a reaction", icon_url=user.avatar_url)
            await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        now = datetime.datetime.now()
        if reaction.message.attachments:
            attachment_link = reaction.message.attachments[0].url
            kiirando_uzenet = f"{user.name} has removed {reaction.emoji} from " \
                              f"{reaction.message.author}'s message in channel " \
                              f"{reaction.message.channel.mention}: {attachment_link}"
        else:
            kiirando_uzenet = f"{user.name} has removed {reaction.emoji} from {reaction.message.author}'s " \
                              f"message in channel {reaction.message.channel.mention}: {reaction.message.content}"
        embed = discord.Embed(
            title=f"``{now}:``",
            description=f"{kiirando_uzenet}",
            colour=discord.Colour.dark_teal()
        )
        embed.set_thumbnail(url=reaction.message.author.avatar_url)
        embed.set_author(name=user.name + " has removed a reaction", icon_url=user.avatar_url)
        await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # ezt azért raktam ide, mert az id vizsgálatánál egyes esetekben errort ad
        # pl: on_voice_state_update error: 'NoneType' object has no attribute 'guild'
        if not member.bot:
            db = Database()
            now = datetime.datetime.now()
            kiirhato = True
            nem_mute_az_event_oka = (bool((before.deaf == after.deaf) and (before.mute == after.mute)
                                          and (before.self_deaf == after.self_deaf)
                                          and (before.self_mute == after.self_mute)
                                          and (member.id != 549654750585421825)))
            if (before.channel is None) and (after.channel.guild.id == 399595937409925140) and nem_mute_az_event_oka:
                uzenet = f"**{member.name}** has just joined **{after.channel.name}**"
                db.update_last_in_voice(member.id)  # updating last seen time in the database...
            elif ((before.channel.guild.id == 399595937409925140) and (after.channel is None)
                    and nem_mute_az_event_oka):
                uzenet = f"**{member.name}** has just disconnected from **{before.channel.name}** " \
                         f"after {db.calculate_time_spent_in_voice(member.id)}"  # printing time in voice...
            elif ((before.channel.guild.id != 399595937409925140) and
                    (after.channel.guild.id == 399595937409925140) and nem_mute_az_event_oka):
                uzenet = f"**{member.name}** has just joined **{after.channel.name}**"
                db.update_last_in_voice(member.id)  # updating last seen time in the database...
            elif ((before.channel.guild.id == 399595937409925140) and
                    (after.channel.guild.id == 399595937409925140) and nem_mute_az_event_oka):
                uzenet = f"**{member.name}** has moved from **{before.channel.name}** to **{after.channel.name}**"
            else:
                uzenet = None
                kiirhato = False

            if kiirhato:
                # checking whether the member who updated their voice state has birthday today
                if db.check_birthday(member.id, now.year, now.month, now.day):
                    await self.bot.get_channel(484010396076998686).send(f"Boldog szülinapot, {member.mention}! "
                                                                        f":birthday: :tada:")
                embed = discord.Embed(
                    title=f"``{now}:``",
                    description=f"{uzenet}",
                    colour=discord.Colour.blue()
                )
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_author(name=f"{member.name} has updated their VoiceState", icon_url=member.avatar_url)
                await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        now = datetime.datetime.now()
        if invite.max_age == 0:
            expires_in = "doesn't have an expiration time set"
        else:
            expires_in = f"will expire in {round(invite.max_age / 3600, 2)} hour(s)"  # max_age is in seconds
        embed = discord.Embed(
            title=f"``{now}:``",
            description=f"{invite.inviter.mention} has just created the invite *{invite.code}* for channel "
                        f"{invite.channel.name}, which {expires_in}, and may be used {invite.max_uses} times.",
            colour=discord.Colour.dark_orange()
        )
        embed.set_thumbnail(url=invite.inviter.avatar_url)
        embed.set_author(name=f"{invite.inviter.name} has just created an invite", icon_url=invite.inviter.avatar_url)
        await self.bot.get_channel(550724640469942285).send(embed=embed)

    # TODO: command error vs on_error?
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # derived from discord.ext.commands.ExtensionError
        if isinstance(error, commands.ExtensionNotFound):
            err = "A modul nem található."
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            err = "A betölteni kívánt modul már be van töltve."
        elif isinstance(error, commands.ExtensionNotLoaded):
            err = "A használni kívánt modul nincs betöltve."
        elif isinstance(error, commands.NoEntryPointError):
            err = "A betölteni kívánt modul nem rendelkezik 'setup' függvénnyel."
        # derived from discord.ext.commands.CommandError
        elif isinstance(error, commands.CommandNotFound):
            err = "A beírt parancs nem létezik."
        elif isinstance(error, commands.TooManyArguments):
            err = "Túl sok paramétert adtál meg."
        elif isinstance(error, commands.MissingRequiredArgument):
            err = "Nem adtál meg minden szükséges paramétert."
        elif isinstance(error, commands.BadArgument):
            err = "Nem megfelelő paramétereket adtál meg."
        elif isinstance(error, commands.UserInputError):
            err = "Nem jól adtad meg a parancsot."
        elif isinstance(error, commands.CheckFailure):
            err = "Hiba a jogosultságok ellenőrzése során."
        elif isinstance(error, commands.CommandInvokeError):
            err = "Hiba a meghívott parancsban."
        elif isinstance(error, commands.CommandError):
            err = "Hiba a parancs futtatása során."
        # any other error is highly unlikely, but this should be able to handle them in case it's needed
        else:
            err = "Ismeretlen hiba."
        now = datetime.datetime.now()
        embed = discord.Embed(
            title=f"``{now}:`` ",
            description=f":interrobang: {err}",
            colour=discord.Colour.from_rgb(255, 0, 13)
        )
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_author(name="Command error",
                         icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter"
                                  "/185/cross-mark_274c.png")
        embed.add_field(name="Error message:", value=f"{error}", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
