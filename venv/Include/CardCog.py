import random
from discord.ext import commands
from BotHelperFunctions import get_roll_range
from Game import Game


class Card(commands.Cog, name="Card"):
    g = Game()

    def __init__(self, client):
        self.client = client

    @commands.command(name="card")
    async def card(self, ctx):
        chat_channel = 0
        check = False
        msg = ''
        players = []
        ch_test = ctx.author.voice
        if ch_test is not None:
            chat_channel = ch_test.channel
            players_m = chat_channel.members
            if len(players_m) >= 1:
                for p in players_m:
                    players.append(p.name)
                    msg = self.g.play(players, 1)
        else:
            msg = f"**{ctx.author.name}** : {self.g.get_random_card()}"
        await ctx.channel.send(msg)


def setup(client):
    client.add_cog(Card(client))
