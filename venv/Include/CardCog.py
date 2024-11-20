import random

import discord
from discord.ext import commands
from Game import Game


class Card(commands.Cog, name="Card"):
    g = Game()

    def __init__(self, client):
        self.client = client
    card_desc="draws cards"
    card_help_brief="draws cards for all users in voice channel"
    card_help_long="Draws a card for each user currently in the same voice channel as the sending user.The card with " \
                   "the highest rank is the winner(Very Exciting, I know)If not connected to a voice channel, " \
                   "draws a single card for the user and outputs value into the text channel where the command was " \
                   "sent from "

    @commands.command(name="card",description=card_desc,help=card_help_long,brief=card_help_brief)
    async def card(self, ctx):
        chat_channel = 0
        check = False
        msg = ''
        header = '---Highest Card---'
        max_msg_length=2000
        max_embed_length=4096
        players = []
        current_channel = ctx.author.voice
        if current_channel is not None:
            chat_channel = current_channel.channel
            players_m = chat_channel.members
            if self.client.user in players_m:
                players_m.remove(self.client.user)
            print(len(players_m))
            if len(players_m) >= 1:
                for p in players_m:
                    players.append(p.name)
                msg = self.g.play(players, 1)
                if (len(header)+len(msg))<=max_embed_length:
                    emb = discord.Embed(title=header,
                                        description=msg,
                                        color=discord.Color.dark_blue())
                    emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    await ctx.channel.send(embed=emb)

        else:
            #msg = f"**{ctx.author.name}** : {self.g.get_random_card()}"
            #await ctx.channel.send(msg)
            emb = discord.Embed(
                title=f'{self.g.get_random_card()}',
                #description='',
                color=discord.Color.dark_blue())
            emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            await ctx.channel.send(embed=emb)



def setup(client):
    client.add_cog(Card(client))
