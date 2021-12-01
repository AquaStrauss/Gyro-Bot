import config
import os

from discord.ext import commands as cmd


#Initialisation
bot = cmd.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print("Bot Initiated !")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

#PING
@bot.command()
async def ping(ctx):
    await ctx.send("Pong. :ping_pong:")
    

bot.run(config.apikeydiscord)