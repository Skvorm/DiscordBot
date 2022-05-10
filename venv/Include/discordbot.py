import discord
import datetime as dt
from BotHelperFunctions import *
from dotenv import load_dotenv
from discord.ext import commands

sv_intents = discord.Intents.all()
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot_GUILD = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix='!', intents=sv_intents)
client.load_extension("MediaCog")
client.load_extension("RollCog")
client.load_extension("CardCog")

#print(f'responding to commands starting with"{client.command_prefix}"')
#for c in client.commands:
    #print(f'{c.name}:{c.enabled}')

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

if __name__ == '__main__':
    time = dt.datetime.now()
    print(f"starting client:{time.strftime('%c')}")
    try:
        client.run(token)
    except Exception as e:
        print("couldn't connect")
