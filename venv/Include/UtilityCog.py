import discord.ext.commands
from discord.ext import commands, bridge


class Utils(commands.Cog, name="Utils"):
    def __init__(self, client: discord.ext.commands.Bot):
        self.client = client

    @bridge.bridge_command()
    async def ping(self, ctx):
        if type(ctx) is discord.commands.context.ApplicationContext:
            await ctx.respond(f"Current Ping:{self.client.latency}")
        else:
            await ctx.send(f"Current Ping:{self.client.latency}")




def setup(client):
    client.add_cog(Utils(client))
