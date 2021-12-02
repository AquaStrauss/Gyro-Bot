import config
import requests
import json
import discord
from discord.ext import commands as cmd
from pycoingecko import CoinGeckoAPI
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

gecko = CoinGeckoAPI()


class CoinInformation(cmd.Cog, name="Token Information "):

    def __init__(self, bot):
        self.client=bot
        
    #COINGECKO
    @cmd.command(brief="Give different informations about Gyro.")
    async def gyro(self, ctx):
        coinInfo=gecko.get_coin_by_id(id="gyro")

        #GET THE ACTUAL PRICE
        headers = {
            'accept': 'application/json',
            'X-API-Key': f'{config.apikeyMoralis}',
        }
        params = (
            ('chain', 'bsc'),
        )
        responseMoralis = requests.get('https://deep-index.moralis.io/api/v2/erc20/0x1b239abe619e74232c827fbe5e49a4c072bd869d/price', headers=headers, params=params)

        responseContent=json.loads(responseMoralis.text)
        price=round(responseContent['usdPrice'],2)

        #GET THE ACTUAL RFV + Circulating Supply + APY
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
            treasuryRiskFreeValue
            gyroCirculatingSupply
            currentAPY
        }
        }
        ''')
        responseGQL = client.execute(query)

        apy=round(float(responseGQL['protocolMetrics'][0]['currentAPY']),2)

        #MATH THE ACTUAL RFV : RFV TREASURY / TOTAL SUPPLY
        rfvTreasury=round(float(responseGQL['protocolMetrics'][0]['treasuryRiskFreeValue']),2)
        totalSupply=round(float(responseGQL['protocolMetrics'][0]['gyroCirculatingSupply']),2)
        rfv=round(rfvTreasury/totalSupply,2)

        urlHomepage=coinInfo['links']['homepage'][0]
        urlCommunity=coinInfo['links']['chat_url'][0]

        embed=discord.Embed(title="GYRO", url=urlHomepage)
        embed.set_thumbnail(url=coinInfo['image']['thumb'])

        embed.add_field(name="Rank :", value=f"{coinInfo['market_cap_rank']}", inline=True)
        embed.add_field(name=u"\u200B", value=u"\u200B", inline=True)
        embed.add_field(name="Price :", value=f"{price}$", inline=True)

        embed.add_field(name="24h :", value=f"{round(coinInfo['market_data']['price_change_percentage_24h'],2)}%", inline=True)
        embed.add_field(name=u"\u200B", value=u"\u200B", inline=True)
        embed.add_field(name="7D :", value=f"{round(coinInfo['market_data']['price_change_percentage_7d'],2)}%", inline=True)

        embed.add_field(name="RFV :", value=f"{rfv}$", inline=True)
        embed.add_field(name=u"\u200B", value=u"\u200B", inline=True)
        embed.add_field(name="APY :", value=f"{apy}%", inline=True)

        embed.add_field(name="Market Cap :", value=f"{coinInfo['market_data']['market_cap']['usd']}$", inline=True)
        embed.add_field(name=u"\u200B", value=u"\u200B", inline=True)
        embed.add_field(name="Volume :", value=f"{coinInfo['market_data']['total_volume']['usd']}$", inline=True)

        if coinInfo['links']['homepage'][0]:
            embed.add_field(name="Website :", value=urlHomepage, inline=False)
        if coinInfo['links']['chat_url'][0]:
            embed.add_field(name="Community :", value=urlCommunity, inline=False)

        await ctx.send(embed=embed)

    #PRICE
    @cmd.command(brief="Give the price of Gyro.")
    async def price(self, ctx):
        #GET THE ACTUAL PRICE
        headers = {
            'accept': 'application/json',
            'X-API-Key': f'{config.apikeyMoralis}',
        }
        params = (
            ('chain', 'bsc'),
        )
        response = requests.get('https://deep-index.moralis.io/api/v2/erc20/0x1b239abe619e74232c827fbe5e49a4c072bd869d/price', headers=headers, params=params)

        responseContent=json.loads(response.text)
        price=round(responseContent['usdPrice'],2)

        coinInfo=gecko.get_coin_by_id(id="gyro")

        embed=discord.Embed(title="GYRO :", url=coinInfo['links']['homepage'][0])
        embed.add_field(name="Price :", value=f"**{price}$**", inline=True)
        embed.set_thumbnail(url=coinInfo['image']['large'])

        await ctx.send(embed=embed)

    #RFV
    @cmd.command(brief="Give the actual RFV of Gyro.")
    async def rfv(self, ctx):
        coinInfo=gecko.get_coin_by_id(id="gyro")
        
        #GET THE ACTUAL RFV TREASURY
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
            treasuryRiskFreeValue
            gyroCirculatingSupply
        }
        }
        ''')
        responseGQL = client.execute(query)

        #MATH THE ACTUAL RFV : RFV TREASURY / TOTAL SUPPLY
        rfvTreasury=round(float(responseGQL['protocolMetrics'][0]['treasuryRiskFreeValue']),2)
        totalSupply=round(float(responseGQL['protocolMetrics'][0]['gyroCirculatingSupply']),2)
        rfv=round(rfvTreasury/totalSupply,2)

        embed=discord.Embed(title="GYRO :", url=coinInfo['links']['homepage'][0])
        embed.add_field(name="RFV :", value=f"**{rfv}$**", inline=True)
        embed.set_thumbnail(url=coinInfo['image']['large'])

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CoinInformation(bot))