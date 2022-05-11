from discord.ext import commands


class Utils(commands.Cog, name="Utils"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Current Ping:{self.client.latency}")


def setup(client):
    client.add_cog(Utils(client))
