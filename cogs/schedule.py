import discord
from discord.ext import commands as cmd

import datetime
import json
from dateutil.relativedelta import relativedelta

class Schedule(cmd.Cog, name="Schedule"):

    def __init__(self, bot):
        self.client=bot

    @cmd.command()
    async def newSchedule(self, ctx, name, desc, y, m , d, h, mm):

        with open('data/schedule.json', 'r') as f:
            schedule=json.load(f)

        if not name in schedule:
            schedule[name.upper()] = {}
            schedule[name.upper()]['description'] = desc
            schedule[name.upper()]['year'] = y
            schedule[name.upper()]['month'] = m
            schedule[name.upper()]['day'] = d
            schedule[name.upper()]['hour'] = h
            schedule[name.upper()]['minute'] = mm

            with open('data/schedule.json', 'w') as f:
                f.write(json.dumps(schedule, indent=4, separators=(',', ': ')))

            embed=discord.Embed(title=name.upper(), description=desc)
            embed.add_field(name="Date :", value=f"{m}/{d}/{y} at {h}:{mm}.", inline=True)
            await ctx.send(embed=embed)

        elif name in schedule:
            await ctx.send(f"Already having a schedule with this name.")

        else:
            await ctx.send(f"Impossible to add the schedule : {name.upper()} !")

    @cmd.command()
    async def until(self, ctx, name):

        currentDT=datetime.datetime.now()

        with open('data/schedule.json', 'r') as f:
            schedule=json.load(f)
            desc = str(schedule[name.upper()]['description'])
            y = int(schedule[name.upper()]['year'])
            m = int(schedule[name.upper()]['month'])
            d = int(schedule[name.upper()]['day'])
            h = int(schedule[name.upper()]['hour'])
            mm = int(schedule[name.upper()]['minute'])

            rd = relativedelta(datetime.datetime(y, m, d, h, mm), currentDT)

            embed=discord.Embed(title=name.upper(), description=desc)
            embed.add_field(name="Date :", value=f"{m}/{d}/{y} at {h}:{mm}.", inline=False)
            if rd.years > 0:
                embed.add_field(name="Year :", value=rd.years, inline=True)
            if rd.months > 0 or rd.years > 0:
                embed.add_field(name="Month :", value=rd.months, inline=True)
            if rd.days > 0 or rd.months > 0 or rd.years > 0:
                embed.add_field(name="Day :", value=rd.days, inline=True)
            if rd.hours > 0 or rd.days > 0 or rd.months > 0 or rd.years > 0:   
                embed.add_field(name="Hour : ", value=rd.hours, inline=True)
            if rd.minutes > 0 or rd.hours > 0 or rd.days > 0 or rd.months > 0 or rd.years > 0: 
                embed.add_field(name="Minute :", value=rd.minutes, inline=True)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Schedule(bot))