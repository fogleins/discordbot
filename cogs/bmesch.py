# ez a fájl a szobasch.py újabb és javított változata
import discord
from discord.ext import commands
import datetime
import pygooglechart as chrt
import asyncio

class SzobaSCH(commands.Cog, name = "BME"):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def viz(self, ctx, aliases = ["víz", "water", "v", "w", "folyadek", "folyadék", "sch", "SCH"]):
    #     """Schönherzesch szobaszintű ivóvíz-nyilvántartás"""
    #     # Lakókhoz hozzárendelünk egy számot, hogy hány karton vizet vásároltak
    #     sender = ctx.author
    #     adam_discordid = 162662873980469257
    #     adam2_discordid = 630168614867304459
    #     barni_discordid = 382235633395040258
    #     simi_discordid = 358992693453652000
    #     szobatars = (sender.id == adam_discordid or sender.id == adam2_discordid
    #         or sender.id == barni_discordid or sender.id == simi_discordid)
    #     try:
    #         if szobatars:
    #             file = open('/srv/shared/Simi/programozas/discordbot/0schviz.txt', 'r+')
    #             for line in file:
    #                 # a txt-ben a splitelés miatt tabulátort használunk az datok elkülönítésére (ld. lent)
    #                 data_array = line.split('\t')
    #                 if isinstance(data_array[len(data_array)], int):
    #                     data_array[len(data_array)] = data_array[len(data_array)] + 1
    #                 else:
    #                     # dinamikusan növő tömb kéne
    #                     data_array[len(data_array) + 1] = 1
    #             # TODO: Discordra ki kell írni az eredményt
    #             # TODO: lekérdezés parancs (kiírja a fájlban jelenleg tárolt adatokat)
    #             # TODO: esetleg adminonly lehet a csalások elkerülése érdekében, hogy adott id által
    #                 # vásárolt kartonok számát lehet csökkenteni
    #             # TODO: logsba is ki kell írni (embed) a változást
    #             file.write("Ez a fajl a lakok altal vasarolt asvanyvizes kartonok szamat tartalmazza")
    #             file.write(f'{sender.id}\t({sender.name}):\t{data_array[len(data_array)]}')
    #             file.close()
    #         else:
    #             await ctx.send("Ez a parancs csak az SCH1014 lakói számára érhető el.")
    #     except Exception as e:
    #         await ctx.send(f"Error: {e}")

    # jelentkezés lanoschra + infók
    @commands.command(aliases = ["lan", "LAN"])
    async def lanosch(self, ctx, *arg):
        """2019-es Lanosch CS:GO bajnoksággal kapcsolatos dolgok. Help: ?lanosch help"""
        try:
            arg[0] = arg[0].lower()
        except Exception: # ha üres a string
            pass
        try:
            #ha nem kap paramétert
            if not arg:
                if (ctx.author.id != 194506678966812672):
                    file = open("/srv/shared/Simi/programozas/discordbot/0lanosch.txt", 'r+')
                    volt = False
                    for line in file:
                        line = line.split('\t')[0]
                        if int(line) == ctx.message.author.id:
                            volt = True
                            break
                    if not volt:
                        file.write(f"{ctx.author.id}\t{ctx.author.display_name}\n")
                        role = discord.utils.get(ctx.author.guild.roles, name = 'Lanosch')
                        await ctx.author.add_roles(role)
                        await ctx.send(f"{ctx.author.mention} a jelentkezésed rögzítve.")
                        await ctx.message.delete()
                    else:
                        await ctx.send("Már jelentkeztél korábban.")
                        await ctx.message.delete()
                    file.close()
                else:
                    await ctx.send("Levó, ugye ezt te sem gondoltad komolyan? :upside_down:")
            elif arg[0] == "info":
                await ctx.send("https://lano.sch.bme.hu/csgo-bajnoksag-szabalyzat/")
                await ctx.message.delete()
            elif arg[0] == "help":
                await ctx.send("Használható parancsok:\n-``?lanosch info`` részletes kiírás, szabályzat" +
                    "\n-``?lanosch`` ha jelentkezni szeretnél\n-``?lanosch team`` az eddig jelentkezettek" +
                    " névsora\n-``?lanosch vote [str: szavazat]`` csapatnév javaslata, szavazás csapatnévre" +
                    "\n-``?lanosch results`` a csapatnévszavazás jelenlegi állása\n-``?lanosch maps map1" +
                    " map2 map3`` szavazás mapokra\n-``?lanosch mv`` a mapszavazás jelenlegi állása")
                await ctx.message.delete()
            elif arg[0].startswith("csapat") or arg[0].startswith("team"):
                file = open("/srv/shared/Simi/programozas/discordbot/0lanosch.txt", 'r')
                player_count = 0
                lineup = ""
                for line in file:
                    line = line.split('\t')[1]
                    lineup += line
                    player_count += 1
                await ctx.message.delete()
                embed = discord.Embed(
                    title = "Eddig jelentkeztek:",
                    description = f"\n{lineup}",
                    colour = discord.Colour.green()
                )
                embed.set_thumbnail(url = ctx.message.guild.icon_url)
                embed.set_author(name = "Lanosch CS:GO 2019", icon_url = ctx.author.avatar_url)
                if player_count >= 7:
                    embed.add_field(name = "Sokan vagyunk", value = f"Mivel eddig {player_count} fő " +
                    "jelentkezett, így már cseréink is vannak. Ettől függetlenül nyugodtan " +
                    "jelentkezz te is, a lineupot meccsenként lehet változtatni. A végleges " +
                    "felállást majd ezen a Discordon megtaláljátok.", inline = False)
                await self.bot.get_channel(ctx.channel.id).send(embed=embed)
                file.close()
            elif arg[0] == "vote" or arg[0] == "nev":
                file = open("/srv/shared/Simi/programozas/discordbot/0lanoschnev.txt", 'r')
                szavazat = str.join(" ", arg[1:])
                volt = False
                try:
                    # a sorok száma
                    meret = 0
                    n = 0
                    # végigmegyünk a fájl összes során
                    sor = file.readline()[:-1]
                    while sor and sor != '\n':
                        meret += 1
                        sor = file.readline()[:-1]
                    file.close()
                    # meglehetősen nem hatékony, de while-ban nem tudok értéket adni :(
                    fp = open("/srv/shared/Simi/programozas/discordbot/0lanoschnev.txt", 'r')
                    intarray = []
                    strarray = []
                    if meret > 0:
                        for x in range(meret):
                            line = fp.readline()[:-1].split('\t')
                            # ezzel itt gondok lehetnek # már nem
                            intarray.append(int(line[0]))
                            strarray.append(str.join(" ", line[1:]))
                            # végigmegyünk a tömb összes elemén
                        for y in range(len(intarray)):
                            if szavazat == strarray[y]:
                                volt = True
                                n = y
                                break
                        if volt:
                            intarray[n] += 1
                        else:
                            intarray.append(1)
                            strarray.append(szavazat)
                    else:
                        intarray.append(1)
                        strarray.append(szavazat)
                    fp.close()
                    fp = open("/srv/shared/Simi/programozas/discordbot/0lanoschnev.txt", 'w')
                    kivan = []
                    count = 0
                    for count in range(len(intarray)):
                        kivan.append(str(f"{intarray[count]}\t{strarray[count]}\n"))
                    fp.writelines(kivan)
                    await ctx.message.add_reaction(u"\U0001F44C")
                    fp.close()
                except Exception as e:
                    ctx.send(f"Error: {e}")
            elif arg[0] == "votes" or arg[0] == "állás" or arg[0] == "allas" or arg[0] == "results":
                try:
                    file = open("/srv/shared/Simi/programozas/discordbot/0lanoschnev.txt", 'r')
                    volt = False
                    # a sorok száma
                    meret = 0
                    n = 0
                    # végigmegyünk a fájl összes során
                    sor = file.readline()[:-1]
                    while sor and sor != '\n':
                        meret += 1
                        sor = file.readline()[:-1]
                    file.close()
                    # meglehetősen nem hatékony, de while-ban nem tudok értéket adni :(
                    fp = open("/srv/shared/Simi/programozas/discordbot/0lanoschnev.txt", 'r')
                    intarray = []
                    strarray = []
                    if meret > 0:
                        for x in range(meret):
                            line = fp.readline()[:-1].split('\t')
                            # ezzel itt gondok lehetnek # már nem
                            intarray.append(int(line[0]))
                            strarray.append(str.join(" ", line[1:]))
                    else:
                        pass
                    fp.close()
                    # DIAGRAM
                    chart = chrt.PieChart3D(700, 400)
                    chart.set_title("Csapatnévszavazás állása")
                    # chart.set_colours([
                    #     'FF8C00', # darkorange
                    #     'FFFF00', # yellow
                    #     'DC143C', # crimson
                    #     '32CD32', # limegreen
                    #     '00CED1', # darkturquoise
                    #     'B0C4DE', # lightsteelblue
                    #     'BA55D3', # mediumorchid
                    #     '808080', # gray
                    #     'D2691E', # chocolate
                    #     '008080' # teal
                    #     ])
                    # random színek githubról https://gist.github.com/mucar/3898821
                    chart.set_colours([
                        'FF6633', 'FFB399', 'FF33FF', 'FFFF99', '00B3E6',
                        'E6B333', '3366E6', '999966', '99FF99', 'B34D4D',
                        '80B300', '809900', 'E6B3B3', '6680B3', '66991A',
                        'FF99E6', 'CCFF1A', 'FF1A66', 'E6331A', '33FFCC',
                        '66994D', 'B366CC', '4D8000', 'B33300', 'CC80CC',
                        '66664D', '991AFF', 'E666FF', '4DB3FF', '1AB399',
                        'E666B3', '33991A', 'CC9999', 'B3B31A', '00E680',
                        '4D8066', '809980', 'E6FF80', '1AFF33', '999933',
                        'FF3380', 'CCCC00', '66E64D', '4D80CC', '9900B3',
                        'E64D66', '4DB380', 'FF4D4D', '99E6E6', '6666FF'
                    ])
                    chart.set_title_style(colour = '000000', font_size = 20)
                    chart.add_data(intarray)
                    chart.set_pie_labels(strarray)
                    # ctx.send(file = "chart.png")
                    chart.download("/srv/shared/Simi/programozas/discordbot/chart.png")
                    #legenerálódjon a fájl
                    await asyncio.sleep(0.125)
                    osszes_szavazat = 0
                    for szavazat in range(len(intarray)):
                        osszes_szavazat += intarray[szavazat]
                    szavazat_aranyok = ""
                    for i in range(len(intarray)):
                        szavazat_aranyok += f"**{strarray[i]}**    {round((intarray[i] / osszes_szavazat * 100), 2)}%\n"
                    kep = discord.File("/srv/shared/Simi/programozas/discordbot/chart.png")
                    await ctx.send(file = kep)
                    # EMBED
                    # küldje el a képet
                    await asyncio.sleep(0.15)
                    embed = discord.Embed(
                        title = "Jelenlegi eredmények:",
                        description = f"\n{szavazat_aranyok}",
                        colour = discord.Colour.green()
                    )
                    # embed.set_image(url = "file:///srv/shared/Simi/programozas/discordbot/chart.png")
                    embed.set_thumbnail(url = ctx.message.guild.icon_url)
                    embed.set_author(name = "Lanosch CS:GO 2019", icon_url = ctx.author.avatar_url)
                    # embed.add_field(name = "Sokan vagyunk", value = f"Mivel eddig {player_count} fő " +
                    # "jelentkezett, így már cseréink is vannak. Ettől függetlenül nyugodtan " +
                    # "jelentkezz te is, a lineupot meccsenként lehet változtatni. A végleges " +
                    # "felállást majd ezen a Discordon megtaláljátok.", inline = False)
                    await self.bot.get_channel(ctx.channel.id).send(embed=embed)
                except Exception as err:
                    print(f"Error: {err}")
    ##########################################################################################################
    ########################################### MAPOS RÉSZ ###################################################
    ##########################################################################################################
            elif arg[0] == "map" or arg[0] == "votemap" or arg[0] == "maps":
                # MAP SZAVAZÁS
                try:    
                    if len(arg) == 4:
                        file = open("/srv/shared/Simi/programozas/discordbot/0lanoschmaps.txt", 'r')
                        volt = False # ha volt már ilyen szavazat a txtben
                        meret = 0
                        n = 0
                        intarray = [] # szavazatok száma
                        strarray = [] # szavazatok stringje
                        # végigmegyünk a fájl összes során, meret a sorok szama
                        sor = file.readline()[:-1]
                        while sor and sor != '\n':
                            meret += 1
                            sor = file.readline()[:-1]
                        file.close()
                        # meglehetősen nem hatékony, de while-ban nem tudok értéket adni :(
                        file = open("/srv/shared/Simi/programozas/discordbot/0lanoschmaps.txt", 'r')
                        # fajl_hossza = 0
                        # beolvassuk a txtben lévő adatokat, majd összevetjük a tömbök tartalmával
                        # ha van már ilyen, akkor int++, különben strarray.append(szavazat)
                        # egy szavazat alkalmával 3x
                        for sor in file:
                            sor = sor.split('\t')
                            intarray.append(int(sor[0]))
                            strarray.append(str(sor[1])[:-1].upper())
                        length = len(strarray) + 2
                        # egy szavazat eleme
                        if meret > 0:
                            for i in range(1, 4): # 0, 1, 2
                                # egy sor
                                # index = 0
                                volt = False
                                length = len(strarray)
                                for egysor in range(length):
                                    if len(strarray) > 0:
                                        if arg[i].upper() == strarray[egysor].upper():
                                            intarray[egysor] += 1
                                            volt = True
                                            break
                                if not volt:
                                    strarray.append(arg[i].upper())
                                    intarray.append(1)
                                    # index += 1
                        else:
                            for n in range(1, 4):
                                strarray.append(arg[n].upper())
                                intarray.append(1)
                        file.close()
                        kiir = open("/srv/shared/Simi/programozas/discordbot/0lanoschmaps.txt", 'w')
                        kimenet = []
                        for j in range(len(intarray)):
                            kimenet.append(str(f"{intarray[j]}\t{strarray[j]}\n").upper())
                        kiir.writelines(kimenet)
                        kiir.close()
                        await ctx.message.add_reaction(u"\U0001F44C")
                    else:
                        await ctx.send("Pontosan 3 mapot adj meg")
                except Exception as err:
                    await ctx.send(f"Error: {err}")
            elif arg[0] == "mapresults" or arg[0] == "mapvotes" or arg[0] == "mv": 
                #MAPSZAVAZÁS EREDMÉNYEI
                try:
                    file = open("/srv/shared/Simi/programozas/discordbot/0lanoschmaps.txt", 'r')
                    volt = False
                    # a sorok száma
                    meret = 0
                    n = 0
                    # végigmegyünk a fájl összes során
                    sor = file.readline()[:-1]
                    while sor and sor != '\n':
                        meret += 1
                        sor = file.readline()[:-1]
                    file.close()
                    # meglehetősen nem hatékony, de while-ban nem tudok értéket adni :(
                    fp = open("/srv/shared/Simi/programozas/discordbot/0lanoschmaps.txt", 'r')
                    intarray = []
                    strarray = []
                    if meret > 0:
                        for x in range(meret):
                            line = fp.readline()[:-1].split('\t')
                            # ezzel itt gondok lehetnek # már nem
                            intarray.append(int(line[0]))
                            strarray.append(str(line[1]))
                    else:
                        pass
                    fp.close()
                    # DIAGRAM
                    chart = chrt.PieChart3D(700, 400)
                    chart.set_title("Map szavazatok")
                    chart.set_colours([
                        'FF6633', 'FFB399', 'FF33FF', 'FFFF99', '00B3E6',
                        'E6B333', '3366E6', '999966', '99FF99', 'B34D4D',
                        '80B300', '809900', 'E6B3B3', '6680B3', '66991A',
                        'FF99E6', 'CCFF1A', 'FF1A66', 'E6331A', '33FFCC',
                        '66994D', 'B366CC', '4D8000', 'B33300', 'CC80CC',
                        '66664D', '991AFF', 'E666FF', '4DB3FF', '1AB399',
                        'E666B3', '33991A', 'CC9999', 'B3B31A', '00E680',
                        '4D8066', '809980', 'E6FF80', '1AFF33', '999933',
                        'FF3380', 'CCCC00', '66E64D', '4D80CC', '9900B3',
                        'E64D66', '4DB380', 'FF4D4D', '99E6E6', '6666FF'
                    ])
                    chart.set_title_style(colour = '000000', font_size = 20)
                    chart.add_data(intarray)
                    chart.set_pie_labels(strarray)
                    chart.download("/srv/shared/Simi/programozas/discordbot/mapchart.png")
                    # legenerálódjon a fájl
                    await asyncio.sleep(0.125)
                    osszes_szavazat = 0
                    for szavazat in range(len(intarray)):
                        osszes_szavazat += intarray[szavazat]
                    szavazat_aranyok = ""
                    for i in range(len(intarray)):
                        szavazat_aranyok += f"**{strarray[i]}**    {round((intarray[i] / osszes_szavazat * 100), 2)}%\n"
                    kep = discord.File("/srv/shared/Simi/programozas/discordbot/mapchart.png")
                    await ctx.send(file = kep)
                    # EMBED
                    # küldje el a képet
                    await asyncio.sleep(0.15)
                    embed = discord.Embed(
                        title = "Jelenlegi mapszavazás-eredmények:",
                        description = f"\n{szavazat_aranyok}",
                        colour = discord.Colour.green()
                    )
                    embed.set_thumbnail(url = ctx.message.guild.icon_url)
                    embed.set_author(name = "Lanosch CS:GO 2019", icon_url = ctx.author.avatar_url)
                    await self.bot.get_channel(ctx.channel.id).send(embed=embed)
                except Exception as err:
                    print(f"Error: {err}")
            else:
                await ctx.send("A ?lanosch parancsnak nincs ilyen paramétere.", delete_after = 10)
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(SzobaSCH(bot))