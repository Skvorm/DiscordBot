import datetime as dt
import discord
from discord.ext.commands import CommandNotFound
from discord.ext import commands, bridge
from BotHelperFunctions import *
from dotenv import load_dotenv


sv_intents = discord.Intents.all()
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot_GUILD = os.getenv('DISCORD_GUILD')
debug_guild = [os.getenv('GUILD_ID')]
client = bridge.Bot(debug_guild=debug_guild, command_prefix='!', intents=sv_intents)
client.load_extension("MediaCog")
client.load_extension("RollCog")
client.load_extension("CardCog")
client.load_extension("UtilityCog")


@client.event
async def on_ready():
    print(f"{client.user.name} connected")
    print(os.getcwd())


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        pass


if __name__ == '__main__':
    time = dt.datetime.now()
    print(f"starting client:{time.strftime('%c')}")
    try:
        client.run(token)
    except Exception as e:
        print("couldn't connect")
