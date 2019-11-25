import random
import datetime
import asyncio
import discord
from discord.ext import commands

class Experimental(commands.Cog, name = "Experimental"):

    def __init__(self, bot):
        self.bot = bot

    #just wanna see if it really works
    #it doesnt
    # @commands.Cog.listener()
    # async def on_typing(self, ctx, channel, user, when):
    #     rnd = random.randint(1, 2)
    #     if rnd == 1:
    #         uzenet = "{} Yo, {} do you really wanna send that? :flushed: ".format(when, user.display_name)
    #     elif rnd == 2:
    #         uzenet = "Hey, {} are you sure? :thinking:".format(user.display_name)
    #     await ctx.send("{}".format(uzenet), delete_after = 3)

    #maybe bot.on_error??
    @commands.Cog.listener()
    # async def on_error(self, event, *args, **kwargs):
    async def on_error(self, event):
        now = datetime.datetime.now()
        try:
            # try:
            #     args_str = args
            # except Exception:
            #     args_str = " "
            # try:
            #     kwargs_str = kwargs
            # except Exception:
            #     kwargs_str = " "
            embed = discord.Embed(
                title=f'``{now}:`` ',
                description=(f":interrobang: Non-command error: {event} rasied an exception:"),# +
                    #f" args: {args_str}; kwargs: {kwargs_str}"),
                colour=discord.Colour.from_rgb(255, 0, 13)
            )
            embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/URc4P573HFyaYe6vysVJ5GDeG4yf675sa-vT9IjYMao/%\3Fsize%3D1024/https/cdn.discordapp.com/icons/399595937409925140/b80c7368fbb679d750c7c0809295a555.webp')
            embed.set_author(name='Non-command error', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/185/cross-mark_274c.png')
            await self.bot.get_channel(550724640469942285).send(embed = embed)
        except Exception as e:
            print(f"Non-command error. Couldn't send an error message to the logs channel. ({e})")

    #PMek kezelése (?)
    #note: rewriteban erre elvileg van külön event
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != message.guild.id:
            #ascii emojis
            try:
                ch = message.channel
                if message.content.startswith("\\shrug"):
                    await message.delete()
                    await ch.send("¯\\_(ツ)_/¯")
                elif message.content.startswith("\\tableflip"):
                    await message.delete()
                    await ch.send("(╯°□°）╯︵ ┻━┻")
                elif message.content.startswith("\\unflip"):
                    await message.delete()
                    await ch.send("┬─┬ ノ( ゜-゜ノ)")
                elif message.content.startswith("\\lenny"):
                    await message.delete()
                    await ch.send("( ͡° ͜ʖ ͡°)")
                elif message.content.startswith("\\wat"): #Want-A-Taco
                    await message.delete()
                    #kikommentelt rész nagyjából jó, csak kicsit nagy
                        #a sorok közötti távolság
                    # await ch.send("{\\__\/}")
                    # await ch.send("(●_●)")
                    # await ch.send("( >🌮 Want a taco?")
                    #ez talán még jobb
                    # await ch.send("{\\\_\_\/}\n(●\_●)\n( >🌮 Want a taco?")
                    await ch.send("{\\\_\/}\n(●\_●)\n( >🌮 Want a taco?")
                elif message.content.startswith("\\"): #hierarchiában lejjebb van, így a fentieknél nem fut le
                    await ch.send(f"Command {message.content} does not exist.")
                else:
                    pass
            except Exception as e:
                print("Error: " + e)
        else: #ha PM
            uzenet = message.content
            felado = message.author
            await self.bot.get_channel(358992693453652000).send(f'{felado}: {uzenet}')

    # #helyi fájl lejátszása
    # #név nem lehet play cogs.music miatt
    # #HA COGS.MUSIC IS BE LESZ TÖLTVE, A NEVEKET VÁLTOZTATNI KELL!!!!!
    # @commands.command(aliases = ['p', 'pf', 'playfile'])
    # async def play(self, ctx, *, arg):
    #     now = datetime.datetime.now()
    #     szam = arg.lower()
    #     #file path:
    #     fp = ''
    #     artist = ''
    #     song = ''
    #     play = True
    #     randomizalas = False
    #     #arrays
    #     bhop = {'phoon', 'bhop', 'bunnyhop', 'cs', 'csgo'}
    #     babyshark = {'babyshark', 'baby shark', 'shark', 'Baby Shark Dance'.lower()}
    #     lapostetu = {'lt', 'ltetű', 'lapos tetű', 'lapos tetu', 'lapost', 'lapostetű'}
    #     shakethat = {'shake', 'st', 'shakethat'}
    #     roblox = {'roblox', 'oof', 'r'}
    #     nevada = {'nevada'}
    #     bigd = {'bigd', 'big dick', 'dick', 'dick song'}
    #     remedy = {'remedy', 'alesso', 'alesso - remedy'}
    #     numberone = {'numberone', 'n1', 'no1', 'number one', 'number one', 'lazy town'}
    #     clinteastwood = {'clint eastwood', 'gorillaz', 'gz', 'ce'}
    #     coconut = {'coconut', 'c', 'the coconut song', 'coconut song'}
    #     tobbturelem = {'több türelem', 'tt', 'tobb turelem', 'többtürelem'}
    #     soldi = {'soldi', 'mahmood'}
    #     #commandok feldolgozása
    #     if szam == 'moms spaghetti' or szam == 'spaghetti' or szam == 'mums spaghetti' or szam == 'ms':
    #         fp = '/mnt/torrent/rwLive/songs/momsspaghetti.mp3'
    #         artist = 'Eminem'
    #         song = "'Mom's spaghetti' (Lose Yourself *cover*)"
    #     elif szam in bhop:
    #         fp = '/mnt/torrent/rwLive/songs/bhop.mp3'
    #         artist = 'La Caution'
    #         song = 'Thé À La Menthe (aka bhop music)'
    #     elif szam in babyshark:
    #         fp = '/mnt/torrent/rwLive/songs/babyshark.mp3'
    #         artist = 'Pinkfong'
    #         song = 'Baby Shark'
    #     elif szam in lapostetu:
    #         fp = '/mnt/torrent/rwLive/songs/lapostetu.mp3'
    #         artist = 'Unknown Artist'
    #         song = 'Lapostetű'
    #     elif szam in shakethat:
    #         fp = '/mnt/torrent/rwLive/songs/shakethat.mp3'
    #         artist = 'Eminem & Nate Dogg'
    #         song = 'Shake That'
    #     elif szam in nevada:
    #         fp = '/mnt/torrent/rwLive/songs/nevada.mp3'
    #         artist = 'Vicetone & Cozi Zuehlsdorff'
    #         song = 'Nevada'
    #     elif szam in bigd:
    #         fp = '/mnt/torrent/rwLive/songs/bigd.mp3'
    #         artist = 'Littel Big'
    #         song = 'Big D**k'
    #     elif szam in roblox:
    #         fp = '/mnt/torrent/rwLive/songs/roblox.mp3'
    #         artist = 'Roblox'
    #         song = 'Roblox Death sound effect'
    #     elif szam in remedy:
    #         fp = '/mnt/torrent/rwLive/songs/remedy.mp3'
    #         artist = 'Alesso'
    #         song = 'Remedy'
    #     elif szam in numberone:
    #         fp = '/mnt/torrent/rwLive/songs/numberone.mp3'
    #         artist = 'Lazy Town'
    #         song = 'We are Number One (magyarul)'
    #     elif szam in clinteastwood:
    #         fp = '/mnt/torrent/rwLive/songs/clinteastwood.mp3'
    #         artist = 'Gorillaz'
    #         song = 'Clint Eastwood'
    #     elif szam in coconut:
    #         fp = '/mnt/torrent/rwLive/songs/coconut.mp3'
    #         artist = 'Smokey Mountain'
    #         song = 'The Coconut Song'
    #     elif szam in tobbturelem:
    #         fp = '/mnt/torrent/rwLive/songs/tobbturelem.mp3'
    #         artist = 'Hősök x Halott Pénz'
    #         song = 'Több türelem'
    #     elif szam in soldi:
    #         fp = '/mnt/torrent/rwLive/songs/soldi.mp3'
    #         artist = 'Mahmood'
    #         song = 'Soldi'
    #     #add: shake that, lapostetű, nevada, big dick, 8 mile
    #     #gangnam style
    #     #punnany massif, imagine dragons, twenty one pilots
    #     #playlist randomizálással (is)
    #     #while-oknál valami jobb módszert kell taálni
    #     #vagy valahogy értéket adni a voice_clientnek
    #     elif szam == 'random' or szam == 'rnd':
    #         randomizalas = True
    #     #help kilistázza a jelenleg elérhető számokat
    #     elif szam == 'help':
    #         play = False
    #         minimum_role = discord.utils.get(ctx.guild.roles, name='1337')
    #         toprole = ctx.message.author.top_role
    #         if minimum_role >= toprole:
    #             await ctx.send("You can add songs by typing ``?p add songname`` or if your Spotify account" + 
    #                 " is connected with your Discord and you're listening to a song on Spotify, you can" +
    #                 " simply type ``?p add spotify`` or ``?p add sf`` or``?p add sp``" +
    #                 "\nYou can play the following songs:" + 
    #                 "\n-Mom's spaghetti (``?p ms``)" + 
    #                 "\n-Thé À La Menthe (bhop music)(``?p bhop``)" + 
    #                 "\n-Baby shark (``?p babyshark``)" +
    #                 "\n-Lapostetű (``?p lapostetű``)" + 
    #                 "\n-Shake That (``?p shakethat``)" +
    #                 "\n-Nevada (``?p nevada``)" + 
    #                 "\n-Big D**k (``?p bigd``)" + 
    #                 "\n-Remedy (``?p remedy``)" + 
    #                 "\n-Roblox death sound (``?p roblox``)" + 
    #                 "\n-We're number one (magyar) (``?p n1``)" + 
    #                 "\n-Clint Eastwood (``?p ce``)" + 
    #                 "\n-The Coconut Song (``?p coconut``)"
    #                 "\n-Több türelem (``?p tt``)", 
    #                 "\n-Soldi (``?p soldi``)", 
    #                 delete_after = 30)
    #         else:
    #             await ctx.send("You can add songs by typing ``?p add songname``\nYou can play the following" +
    #                 " songs:" + 
    #                 "\n-Mom's spaghetti (``?p ms``)" +
    #                 "\n-Thé À La Menthe (bhop music) (``?p bhop``)" + 
    #                 "\n-Baby shark (``?p babyshark``)" + 
    #                 "\n-Shake That (``?p shakethat``)" + 
    #                 "\n-Nevada (``?p nevada``)" +
    #                 "\n-Remedy (``?p remedy``)" + 
    #                 "\n-We're number one (magyar) (``?p n1``)" + 
    #                 "\n-Clint Eastwood (``?p ce``)" + 
    #                 "\n-The Coconut Song (``?p coconut``)", 
    #                 "\n-Több türelem (``?p tt``)", 
    #                 "\n-Soldi (``?p soldi``)", 
    #                 delete_after = 30)
    #     #Jelenleg hallgatott spotify szám hozzáadása
    #     elif szam.startswith("add spotify") or szam.startswith("add sf") or szam.startswith("add sp"):
    #         play = False
    #         member = ctx.message.author
    #         if member.activity:
    #             if member.activity.name == 'Spotify':
    #                 try:
    #                     spotify = member.activity
    #                     file = open('/mnt/torrent/Simi shared/programozas/discordbot/0localzene.txt', 'a')
    #                     file.write('\n')
    #                     file.write(f'{ctx.author}: {spotify.artist} - {spotify.title}')
    #                     file.close()
    #                     emoji = await ctx.message.guild.fetch_emoji(568431664519446547)
    #                     await ctx.message.add_reaction(emoji)
    #                     await self.bot.get_channel(549709362206081076).send("<@358992693453652000> we've" +
    #                         " got new music to add to local songs!")
    #                     #log + simi
    #                     #await self.bot.get_channel(549709362206081076).send("<@358992693453652000> we've" + 
    #                     # " got new music to add to our playlist!")
    #                     #fstring tördelése így jó???
    #                     uzenet = (f"**{ctx.author.name}** wants to add **{spotify.title}** by" +
    #                         f" **{spotify.artist}** to local songs")
    #                     embed = discord.Embed(title=f'``{now}:``',
    #                         description=f'{uzenet}',
    #                         colour=discord.Colour.green()
    #                     )
    #                     embed.set_thumbnail(url=spotify.album_cover_url)
    #                     embed.set_author(name=ctx.author.name + ' wants to add ' + spotify.title + 
    #                         ' to local songs', 
    #                         icon_url=member.avatar_url)
    #                     await self.bot.get_channel(550724640469942285).send(embed=embed)
    #                 except Exception as e:
    #                     await ctx.send(f"Couldn't add Spotify song to local songs. ({e})")
    #             else:
    #                 await ctx.send("No Spotify listening activity detected.")
    #         else:
    #             await ctx.send("No Spotify listening activity detected.")
    #     elif szam.startswith("add"):
    #         play = False
    #         try:
    #             file = open('/mnt/torrent/Simi shared/programozas/discordbot/0localzene.txt', 'a')
    #             file.write('\n')
    #             file.write(f'{ctx.message.author}: {ctx.message.content}')
    #             file.close()
    #             await ctx.message.add_reaction(u"\U0001F3A7")
    #             await self.bot.get_channel(549709362206081076).send("<@358992693453652000> we've got new" +
    #                 " music to add to local songs!")
    #         except Exception as e:
    #             await ctx.send(f"Couldn't add the song you've suggested. {e}")
    #     else:
    #         play = False
    #         await ctx.send(f"I don't recognise that song ({szam})")
    #     #ha olyan parancs volt, aminek zenét kell lejátszania
    #     if play:
    #         await ctx.message.delete()
    #         #connect
    #         try:
    #             if self.bot.voice_clients:
    #                 voice = ctx.message.guild.voice_client
    #             else:
    #                 voice = await ctx.message.author.voice.channel.connect()
    #         except Exception as e:
    #             await ctx.send(f"Couldn't connect to voice channel. ({e})")
    #         #random
    #         if randomizalas:
    #             try:
    #                 fp_array = [
    #                     '/mnt/torrent/rwLive/songs/momsspaghetti.mp3',
    #                     '/mnt/torrent/rwLive/songs/bhop.mp3', 
    #                     '/mnt/torrent/rwLive/songs/babyshark.mp3',
    #                     '/mnt/torrent/rwLive/songs/shakethat.mp3',
    #                     '/mnt/torrent/rwLive/songs/nevada.mp3',
    #                     '/mnt/torrent/rwLive/songs/remedy.mp3',
    #                     '/mnt/torrent/rwLive/songs/clinteastwood.mp3',
    #                     '/mnt/torrent/rwLive/songs/coconut.mp3',
    #                     '/mnt/torrent/rwLive/songs/tobbturelem.mp3', 
    #                     '/mnt/torrent/rwLive/songs/soldi.mp3'
    #                 ]
    #                 artist_array = [
    #                     'Eminem',
    #                     'La Caution',
    #                     'Pinkfong',
    #                     'Eminem & Nate Dogg',
    #                     'Vicetone & Cozi Zuehlsdorff',
    #                     'Alesso',
    #                     'Gorillaz',
    #                     'Smokey Mountain',
    #                     'Hősök x Halott Pénz', 
    #                     'Mahmood'
    #                 ]
    #                 song_array = [
    #                     "'Mom's spaghetti' (Lose Yourself *cover*)",
    #                     'Thé À La Menthe (aka bhop music)',
    #                     'Baby Shark',
    #                     'Shake That',
    #                     'Nevada',
    #                     'Remedy',
    #                     'Clint Eastwood',
    #                     'The Coconut Song',
    #                     'Több türelem', 
    #                     'Soldi'
    #                 ]
    #                 if ctx.message.guild.voice_client:
    #                     elozo_random = -1
    #                     while ctx.message.guild.voice_client.is_connected():
    #                         random_szam = random.randint(0, len(fp_array) - 1)
    #                         fp = fp_array[random_szam]
    #                         artist = artist_array[random_szam]
    #                         song = song_array[random_szam]
    #                         try:
    #                             voice.play(discord.FFmpegPCMAudio(fp))
    #                             embed = discord.Embed(
    #                                 title=f'``{now}:``',
    #                                 description=(f'Now playing: **{song}** by **{artist}**'),
    #                                 colour=discord.Colour.dark_blue()
    #                             )
    #                             embed.set_thumbnail(url=ctx.author.avatar_url)
    #                             embed.set_author(name='Playback info', icon_url=self.bot.user.avatar_url)
    #                             embed.set_footer(text = f"This song was requested by {ctx.message.author.name}")
    #                             await ctx.send(embed = embed, delete_after = 60)
    #                         except Exception as e:
    #                             await ctx.send(f"Couldn't play the selected song. ({e})")
    #                         #referenced before assignment - elvileg fixed
    #                         while ((ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused())
    #                             and (random_szam != elozo_random)):
    #                                 await asyncio.sleep(10)
    #                         elozo_random = random_szam
    #             except Exception as e:
    #                 if (f"{e}" == "'NoneType' object has no attribute 'is_playing'" 
    #                     or f"{e}" == "'NoneType' object has no attribute 'is_paused'"):
    #                         pass
    #                 else:
    #                     await ctx.send(f"Couldn't play songs randomly. ({e})")
    #         else:
    #             #play
    #             try:
    #                 voice.play(discord.FFmpegPCMAudio(fp))
    #                 embed = discord.Embed(
    #                     title=f'``{now}:`` ',
    #                     description=(f'Now playing: **{song}** by **{artist}**'),
    #                     colour=discord.Colour.dark_blue()
    #                 )
    #                 embed.set_thumbnail(url=ctx.author.avatar_url)
    #                 embed.set_author(name='Playback info', icon_url=self.bot.user.avatar_url)
    #                 embed.set_footer(text = f"This song was requested by {ctx.message.author.name}")
    #                 await ctx.send(embed = embed, delete_after = 60)
    #             except Exception as e:
    #                 await ctx.send(f"Couldn't play the selected song. ({e})")

    # @commands.command(aliases = ['pa'])
    # async def pause(self, ctx):
    #     """Pauses the song that's currently being played."""
    #     guild = ctx.message.guild
    #     message = ctx.message
    #     try:
    #         if guild.voice_client.is_playing():
    #             guild.voice_client.pause()
    #             await message.add_reaction(u"\U0001F44C")
    #             await asyncio.sleep(5)
    #             await ctx.message.delete()
    #         else:
    #             await ctx.send("I'm either not connected to any voice channel or no audio is being played.")
    #     except Exception as e:
    #         await ctx.send(f"Couldn't pause the song. ({e})")
    
    # @commands.command(aliases = ['r', 'res'])
    # async def resume(self, ctx):
    #     """Resumes a paused song."""
    #     guild = ctx.message.guild
    #     message = ctx.message
    #     try:
    #         if guild.voice_client.is_connected():
    #             guild.voice_client.resume()
    #             await message.add_reaction(u"\U0001F44C")
    #             await asyncio.sleep(5)
    #             await ctx.message.delete()
    #         else:
    #             await ctx.send("I'm either not in any voice channel or no song is being played.")
    #         # else:
    #         #     await ctx.send("There's no paused song I could resume playing.") #English?
    #     except Exception as e:
    #         await ctx.send(f"Couldn't resume the song. ({e})")

    # #mivel nincs queue, ezért a skip = stop (music.py.a2r.py 113. sor)
    # @commands.command(aliases = ['st', 'skip', 's']) #HA MUSIC IS BE LESZ TÖLTVE NEVET KELL VÁLTOZTATNI: 
    # # f mint fájl, a yt-os parancsok megkülöböztetésére
    # async def stop(self, ctx):
    #     """Stops the song that's being played, but the bot won't disconnect from the voice channel."""
    #     guild = ctx.message.guild
    #     message = ctx.message
    #     try:
    #         if guild.voice_client.is_connected():
    #             guild.voice_client.stop()
    #             await message.add_reaction(u"\U0001F44C")
    #             await asyncio.sleep(5)
    #             await ctx.message.delete()
    #         else:
    #             await ctx.send("I'm not in any voice channel.")
    #     except Exception as e:
    #         await ctx.send(f"I wasn't able to disconnect. ({e})")

    # @commands.command(aliases = ['join' ,'j'])
    # async def connect(self, ctx):
    #     """Joins the bot into your voice channel."""
    #     try:
    #         if not ctx.guild.voice_client:
    #             await ctx.message.author.voice.channel.connect()
    #             await ctx.message.add_reaction(u"\U0001F44C")
    #             await asyncio.sleep(5)
    #             await ctx.message.delete()
    #         else:
    #             await ctx.send("I'm already in a voice channel.")
    #     except Exception as e:
    #         await ctx.send(f"Error while trying to connect to voice: {e}")

    # @commands.command(aliases =  ['lv', 'leave', 'dc'])
    # async def disconnect(self, ctx):
    #     """Disconnects the LOCAL music player from your voice channel. Local music player is a music player 
    #         that's playing local music files, not YT streams."""
    #     guild = ctx.message.guild
    #     message = ctx.message
    #     try:
    #         if guild.voice_client.is_connected():
    #             await guild.voice_client.disconnect()
    #             await message.add_reaction(u"\U0001F44C")
    #             await asyncio.sleep(5)
    #             await ctx.message.delete()
    #         else:
    #             await ctx.send("I'm not in any voice channel.")
    #     except Exception as e:
    #         await ctx.send(f"I wasn't able to disconnect. ({e})")

    #admin-only reminder
    @commands.command(aliases = ['remind'])
    async def reminder(self, ctx, time, title):
        """Admin-only. Sets a reminder. Syntax: ?remind time[int, in seconds] title[str, between ""]"""
        if ctx.message.author.id == ctx.guild.owner.id:
            try:
                time = int(time)
                title = str(title)
                #emoji https://www.fileformat.info/info/unicode/char/2705/index.htm
                await ctx.message.add_reaction(u"\u2705")
                await asyncio.sleep(time)
                await ctx.send(f"{ctx.guild.owner.mention} you wanted me to remind you to {title}")
            except Exception as e:
                await ctx.send(f"Error creating reminder. ({e})")
        else:
            await ctx.send("This command is admin-only.")

    @commands.command(hidden = True)
    # ahhoz, hogy más szerveren lévő user egyes adatait (pl. 
    # a jelenlegi voice channel nevét, a szerver nevét megkapjuk
    # member helyett user-ként kellene kezelni, de ezeknek nincsenek
    # ilyen attribútumai (pl. user.status, user.voice), így ennek a 
    # parancsnak nem igazán van így értelme)
    #async def tesztusrinfo(self, ctx, member: discord.User): #ez így nem működik
    # helyes megoldás lenne:
    async def tesztusrinfo(self, ctx, member: discord.Member):
        try:
            await ctx.send(f"Name: {member.name}; Status: {member.status};" +
                f" Connected to: {member.voice.channel.name} on {member.voice.channel.guild.name}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    #tesztelésre vár + képeket be kell szerezni
    @commands.command(aliases = ['Kóka', 'kóka'])
    async def koka(self, ctx):
        """Best command to date."""
        rnd = random.randint(1, 4)
        # kep = discord.File(fp = '/mnt/torrent/rwLive/cogs/koka' + str(rnd) + '.jpg')
        kep = discord.File(fp = '/srv/shared/Simi/programozas/discordbot/rwLive/cogs/koka' + str(rnd) + '.jpg')
        await ctx.message.delete()
        await ctx.send(file = kep)

    @commands.command()
    async def playthis(self, ctx, *, url):
        'Plays your most played songs/playlists. (Under testing, might be buggy)'
        message = ctx.message
        teljes_uzenet_splitelve = ctx.message.content.split()
        link = teljes_uzenet_splitelve[len(teljes_uzenet_splitelve) - 1]
        music_bot_channel_id = 443844561270341633
        await self.bot.get_channel(music_bot_channel_id).send(f'!play {link}')
        await message.delete()

    #ugyanaz, mint a spotiplay-nél
    @commands.command(aliases=['kutyafül'])
    async def kokalista(self, ctx):
        'Kóka úr kedvelt YT videóit tartalmazó playlistet kezdi lejátszani'
        lista_url = 'https://www.youtube.com/playlist?list=LLaPUXOjl02GaQKAtRi1KnxQ'
        #channel = ctx.channel
        message = ctx.message
        await self.bot.get_channel(443844561270341633).send(f'!play {lista_url}')
        await message.delete()
        #await ctx.send("I've forwarded your request to Rhytm bot! Your song(s) should start playing in a" +
        #    few seconds. :headphones: ")

    #gyakorlatilag mehet commands.py-ba
    @commands.command(aliases = ['edit', 'limit', 'max']) #max user egy voice channelben
    async def changelimit(self, ctx, limit):
        """Az 'Itt-nem-zavar-a-Szédületes' channelt lehet kisajátítani egy órára. Syntax: ?max [limit(int)]"""
        now = datetime.datetime.now()
        requester = ctx.message.author
        guild = ctx.message.guild
        channel_to_edit = discord.utils.get(guild.voice_channels, name='Itt-nem-zavar-a-Szédületes')
        minimum_role = discord.utils.get(ctx.guild.roles, name='Balaton Squad')
        top_role = requester.top_role
        try:
            limit = int(limit)
        except ValueError as e:
            ctx.send(f":x: Error: You must enter an integer. ({e})", delete_after = 10)
        await ctx.message.delete()
        if top_role >= minimum_role:
            if (limit > 0) and (limit < 99):
                try:
                    await channel_to_edit.edit(user_limit = limit)
                    await ctx.send(f"User limit updated to {limit}. Limit will be set to unlimited in 60" +
                        " minutes.",
                        delete_after = 30)
                    await asyncio.sleep(3300)
                    await ctx.send("User limit will be set to unlimited in 5 minutes.", delete_after = 120)
                    embed = discord.Embed(
                        title=f'``{now}:`` ',
                        description=f'{ctx.author.name} has changed the user limit of' +
                            f' *Itt-nem-zavar-a-Szédületes* to {limit}',
                        colour=discord.Colour.magenta()
                    )
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_author(name='Voice channel user limit updated', icon_url=ctx.author.avatar_url)
                    await self.bot.get_channel(550724640469942285).send(embed = embed)
                    try:
                        await asyncio.sleep(300)
                        await channel_to_edit.edit(user_limit = 0)
                        await ctx.send("User limit has been set to unlimited.", delete_after = 10)
                    except Exception as error:
                        try:
                            await self.bot.get_channel(549709362206081076).send("Couldn't update channel" + 
                                f"user limit. ({error})")
                        except:
                            print(f"Couldn't update channel user limit: {error}")
                except discord.DiscordException as discorderr:
                    await ctx.send(f"Discord error: {discorderr}")
                except Exception as err:
                    try:
                        await ctx.send(f"Error: {err}", delete_after = 30)
                    except Exception as error:
                        print(f"Error: {error}")
            elif (limit < 0) or (limit > 99):
                try:
                    await ctx.send("Limit must be an integer between 1 and 99.", delete_after = 30)
                except Exception:
                    pass
            elif limit == 0:
                try:
                    await channel_to_edit.edit(user_limit = limit)
                    #await ctx.send("Channel user limit has been set to unlimited.")
                    embed = discord.Embed(
                        title=f'``{now}:``',
                        description=f'{ctx.author.name} has set the user limit of' +
                            ' *Itt-nem-zavar-a-Szédületes* to unlimited',
                        colour=discord.Colour.magenta()
                    )
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_author(name='Voice channel user limit updated', icon_url=ctx.author.avatar_url)
                    await ctx.send(embed = embed)
                    await asyncio.sleep(1)
                    await self.bot.get_channel(550724640469942285).send(embed = embed)
                except Exception:
                    pass
        else:
            await ctx.send("You aren't allowed to change the channel's settings.")

    #mivel a music botok nem játszák le amit másik bot kér, ezért csak shortcutnak jó
    @commands.command(aliases = ['splay'])
    async def spotiplay(self, ctx, *args):
        """Sends a play command with the song to which the requester is currently listening to."""
        member = ctx.message.author
        if member.activity:
            if member.activity.name == 'Spotify':
                try:
                    spotify = member.activity
                    await ctx.send(f"!play {spotify.title} by {spotify.artist}", delete_after = 30)
                except Exception:
                    pass
            else:
                try:
                    await ctx.send("No Spotify listening activity detected.", delete_after = 5)
                except Exception:
                    pass
        else:
            try:
                await ctx.send("No Spotify listening activity detected.", delete_after = 5)
            except Exception:
                pass

    #gyakorlatilag mehet commands.py-ba
    @commands.command()
    async def ping(self, ctx):
        """Checks the bot's latency."""
        now = datetime.datetime.now()
        guild = ctx.message.guild
        embed = discord.Embed(
            title=f'``{now}:`` ',
            description = f'Current ping to *{guild.name}* is {round((self.bot.latency * 1000), 2)} ms',
            colour = discord.Colour.blurple()
        )
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name='Pong!', icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f'This message was requested by {ctx.author.name}')
        await ctx.message.delete()
        await ctx.send(embed = embed)

    # sub role automatikus hozzáadása
    @commands.command(hidden = True)
    async def sub(self, ctx):
        try:
            sub_role = discord.utils.get(ctx.guild.roles, name='sub')
            member = ctx.message.author
            await member.add_roles(sub_role)
            await ctx.message.delete()
            await self.bot.get_channel(549709362206081076).send('<@358992693453652000>' +
                f' sub role has been assigned to {member.name}.')
            await ctx.send(f"Hey {member.mention}, access granted!")
        except Exception as error:
            await ctx.send(f"Something went wrong. :( ({error})")

def setup(bot):
    bot.add_cog(Experimental(bot))