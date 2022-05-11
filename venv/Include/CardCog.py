import random
from discord.ext import commands
from Game import Game


class Card(commands.Cog, name="Card"):
    g = Game()

    def __init__(self, client):
        self.client = client
    card_desc="draws cards"
    card_help_brief="draws cards for all users in voice channel"
    card_help_long="Draws a card for each user currently in the same voice channel as the sending user.\
     The card with the highest rank is the winner(Very Exciting, I know)\
    If not connected to a voice channel, draws a single card for the user and outputs value into the text\
     channel where the command was sent from"

    @commands.command(name="card",description=card_desc,help=card_help_long,brief=card_help_brief)
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
