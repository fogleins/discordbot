from discord.ext import commands
from subprocess import Popen, PIPE
from cogs.adminonly import is_admin
from datetime import datetime
from asyncio import sleep


class Hardware(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    report_hdd_temp = False

    @commands.group(invoke_without_command=True)
    async def rbp(self, ctx):  # rbp = raspberry pi
        await ctx.send("This is a command group, which currently has a single subcommand: ``hdd``. "
                       "Syntax: ``?rbp hdd``")

    @rbp.command()
    async def hdd(self, ctx):
        """Prints the HDD's status using HDSentinel"""
        await ctx.message.delete()
        # running the program as sudo is now handled using a shell script
        # for further information, read the following forum thread:
        # https://askubuntu.com/questions/155791/how-do-i-sudo-a-command-in-a-script-without-being-asked-for-a-password
        process = Popen(["sudo /srv/shared/Simi/programozas/discordbot/hdsentinel.sh"], stdout=PIPE, shell=True)
        (output, err) = process.communicate()
        exit_code = process.wait()

        if err is None:
            output = output.decode()    # Converts bytes to str
            output = output.split("\n\n")
            hds_credits = output[0]     # HDS Version...
            hds_startupmessage = output[1]  # Examining...
            output = output[2].split("\n")
            output.pop(2)   # removes the hdd's serial number from the output
            output = "\n".join(output)

            await ctx.send(f"```{hds_credits}\n\n{hds_startupmessage}\n{output}\n\nProgram returned {exit_code}```")
        else:
            await ctx.send(f"Valami :poop:\n{err.decode()}\nExit code: {exit_code}")

    @rbp.command(aliases=["tron"])  # temperature report on
    @commands.check(is_admin)
    async def check_hdd_temp(self, ctx, report_interval: float = 60):
        """Checks the HDD's temperature using HDSentinel
        --------
        :param ctx: The context, in which the command is invoked. This parameter is passed by discordpy automatically
        :param report_interval: The time in minutes, after which the report will be sent
        """
        await ctx.message.delete()
        self.report_hdd_temp = True
        while self.report_hdd_temp:
            # running the program as sudo is now handled using a shell script
            # for further information, read the following forum thread:
            # https://askubuntu.com/questions/155791/how-do-i-sudo-a-command-in-a-script-without-being-asked-for-a-password
            process = Popen(["sudo /srv/shared/Simi/programozas/discordbot/hdsentinel.sh"], stdout=PIPE, shell=True)
            (output, err) = process.communicate()
            exit_code = process.wait()

            if err is None:
                output = output.decode()    # Converts bytes to str
                output = output.split("\n\n")
                hds_credits = f"Hard Disk Sentinel device temperature report\n{output[0]}"     # HDS Version...
                hds_startupmessage = output[1]  # Examining...
                output = output[2].split("\n")
                # output.pop(2)   # removes the hdd's serial number from the output
                temperature = output[6]
                temperature_int = int(temperature[15:17])
                max_temperature = output[7]
                max_temperature_int = int(max_temperature[15:17])
                rep_time = datetime.now()
                output = f"On {rep_time.year}-{rep_time.month}-{rep_time.day} at {rep_time.hour}:{rep_time.minute}:" \
                         f"{rep_time.second}.{rep_time.microsecond}:\n{temperature}\n{max_temperature}"

                await ctx.send(f"```{hds_credits}\n\n{hds_startupmessage}\n{output}```")
                if temperature_int >= max_temperature_int:
                    await ctx.send(f"{ctx.message.author.mention} :triangular_flag_on_post: :thermometer: ")
            else:
                await ctx.send(f"Valami :poop:\n{err.decode()}\nExit code: {exit_code}")
            await sleep(report_interval * 60)

    @rbp.command(aliases=["troff"])  # temperature report off
    @commands.check(is_admin)
    async def hdd_tempreport_off(self, ctx):
        """Turns off the temperature report """
        self.report_hdd_temp = False
        await ctx.message.delete()
        await ctx.send("Temperature reports have been turned off.")

    @rbp.command()
    async def neofetch(self, ctx):
        """Gets the neofetch message and sends it to the Discord channel it was requested in"""
        await ctx.message.delete()
        # Both screenfetch and neofetch return highly formatted results, which do not appear in Discord correctly,
        # therefore this command is implemented for testing purposes only.
        process = Popen(["neofetch"], stdout=PIPE, shell=True)
        (output, err) = process.communicate()
        exit_code = process.wait()

        if err is None:
            output = output.decode()
            await ctx.send(f"```{output}\nProgram returned {exit_code}```")
        else:
            await ctx.send(f"Error: {err.decode()}")


def setup(bot):
    bot.add_cog(Hardware(bot))
