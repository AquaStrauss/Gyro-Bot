from cmath import log
import discord
from discord.ext import commands as cmd
import math
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class Rewards(cmd.Cog, name="Compounding Rewards "):

    def __init__(self, bot):
        self.client=bot

    #APYMATH
    @cmd.command(brief="APY of Gyro.")
    async def apy(self, ctx):

        sample_transport=RequestsHTTPTransport(
            url='https://api.thegraph.com/subgraphs/name/gyro-defi/gyro-subgraph',
            verify=True,
        )

        client = Client(
            transport=sample_transport
        )

        query = gql('''
        query {
        protocolMetrics(first: 1, orderBy: timestamp, orderDirection: desc) {
            currentAPY
        }
        }
        ''')

        response = client.execute(query)

        apy=round(float(response['protocolMetrics'][0]['currentAPY']),2)
        apr = round((math.pow(1+(apy/100),1/1095)-1)*1095,4)

        embed=discord.Embed(title="APY :", description=f"The actual APY of Gyro it's : **{apy}%**", color=0xf5b342)
        embed.add_field(name="APR :", value=f"The actual APR of Gyro it's : **{round(apr*100,2)}%**", inline=True)

        await ctx.send(embed=embed)

    #REWARDS
    @cmd.command(brief="Math the rewards from the actual APY.")
    async def rewards(self, ctx, amount:float=None):

        sample_transport=RequestsHTTPTransport(
            url='https://api.thegraph.com/subgraphs/name/gyro-defi/gyro-subgraph',
            verify=True,
        )
        client = Client(
            transport=sample_transport
        )
        query = gql('''
        query {
        protocolMetrics(first: 1, orderBy: timestamp, orderDirection: desc) {
            currentAPY
        }
        }
        ''')

        response = client.execute(query)
        
        apy=round(float(response['protocolMetrics'][0]['currentAPY']),2)

        if amount:
            apr = round((math.pow(1+(apy/100),1/1095)-1)*1095,4)
            aprRebase = apr/(365*3)
            aprDaily = aprRebase*3

            tomorrowValue = (math.pow(1+(aprRebase),3)-1)*amount
            firstWeekValue = (math.pow(1+aprRebase,7*3)-1)*amount
            firstMonthValue = (math.pow(1+aprRebase,30*3)-1)*amount
            firstQuarterValue = (math.pow(1+aprRebase,90*3)-1)*amount
            firstSemiAnnualValue = (math.pow(1+aprRebase,180*3)-1)*amount
            firstYearValue = (math.pow(1+aprRebase,365*3)-1)*amount

            roiDay = round(math.log(2,1+aprDaily))

            embed=discord.Embed(title="APY :", description=f"If you compound every days, for an APY of `{apy}%` so for an APR of `{round(apr*100,2)}%`, with `{amount}$`.\n**Your ROI will be done after `{roiDay}` days.**", color=0xf5b342)

            embed.add_field(name="-"*8+" Tomorrow "+"-"*8, value=f"**Gain : \n`{round(tomorrowValue,2)}$`\nTotal : \n`{round(tomorrowValue+amount,2)}$`**", inline=True)
            embed.add_field(name="-"*8+" First Week "+"-"*8, value=f"**Gain : \n`{round(firstWeekValue,2)}$`\nTotal : \n`{round(firstWeekValue+amount,2)}$`**", inline=True)
            embed.add_field(name="-"*8+" First Month "+"-"*8, value=f"**Gain : \n`{round(firstMonthValue,2)}$`\nTotal : \n`{round(firstMonthValue+amount,2)}$`**", inline=True)

            embed.add_field(name="-"*7+" First Quarter "+"-"*7, value=f"**Gain : \n`{round(firstQuarterValue,2)}$`\nTotal : \n`{round(firstQuarterValue+amount,2)}$`**", inline=True)
            embed.add_field(name="-"*4+" First Semi-Annual "+"-"*4, value=f"**Gain : \n`{round(firstSemiAnnualValue,2)}$`\nTotal : \n`{round(firstSemiAnnualValue+amount,2)}$`**", inline=True)
            embed.add_field(name="-"*8+" First Year "+"-"*8, value=f"**Gain : \n`{round(firstYearValue,2)}$`\nTotal : \n`{round(firstYearValue+amount,2)}$`**", inline=True)

            await ctx.send(embed=embed)

        else:
            apr = round((math.pow(1+(apy/100),1/1095)-1)*1095,4)
            aprRebase = apr/(365*3)
            aprDaily = aprRebase*3

            daily = round((math.pow(1+(aprRebase),3)-1)*100,4)
            weekly = (math.pow(1+aprRebase,7*3)-1)*100
            monthly = (math.pow(1+aprRebase,30*3)-1)*100
            quartly = (math.pow(1+aprRebase,90*3)-1)*100
            semiAnnually = (math.pow(1+aprRebase,180*3)-1)*100
            yearly = (math.pow(1+aprRebase,365*3)-1)*100

            roiDay = round(math.log(2,1+aprDaily))

            embed=discord.Embed(title="APY :", description=f"If you compound every days, for an APY of `{apy}%` so for an APR of `{round(apr*100,2)}%`.\n**Your ROI will be done after `{roiDay}` days.**", color=0xf5b342)

            embed.add_field(name="-"*8+" Daily "+"-"*8, value=f"**`{round(daily,2)}%`**", inline=True)
            embed.add_field(name="-"*8+" Weekly "+"-"*8, value=f"**`{round(weekly,2)}%`**", inline=True)
            embed.add_field(name="-"*8+" Monthly "+"-"*8, value=f"**`{round(monthly,2)}%`**", inline=True)

            embed.add_field(name="-"*6+" Quarterly "+"-"*6, value=f"**`{round(quartly,2)}%`**", inline=True)
            embed.add_field(name="-"*4+" Semi-Annually "+"-"*4, value=f"**`{round(semiAnnually,2)}%`**", inline=True)
            embed.add_field(name="-"*9+" Yearly "+"-"*9, value=f"**`{round(yearly,2)}%`**", inline=True)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rewards(bot))