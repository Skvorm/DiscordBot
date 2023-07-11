import random

import discord.ext.commands
from discord.ext import commands, bridge
from random import shuffle


class Utils(commands.Cog, name="Utils"):
    def __init__(self, client: discord.ext.commands.Bot):
        self.client = client

    desc = "Divides current users into teams"
    help_brief = "!team [number of teams]"

    @bridge.bridge_command()
    async def ping(self, ctx):
        if type(ctx) is discord.commands.context.ApplicationContext:
            await ctx.respond(f"Current Ping:{self.client.latency}")
        else:
            await ctx.send(f"Current Ping:{self.client.latency}")

    @bridge.bridge_command(
        name="team",
        description="sorts current users into teams",
        cog="Utils",
        help=help_brief,
        brief=help_brief
    )
    async def teams(self, ctx, team_count=2,test=True):
        team_count = int(team_count)
        players = []
        teams = []
        ch_test = ctx.author.voice
        if ch_test is not None:
            chat_channel = ch_test.channel
            players_m = chat_channel.members
            if self.client.user in players_m:
                players_m.remove(self.client.user)
            for t in range(1, team_count + 1):
                teams.append([])
            for p in players_m:
                players.append(p.name)
            if test:
                test_players = ["Bill", "Bob", "Billie Jean", "Bobby", "Larry"]
                for p in test_players:
                    players.append(p)
            random.shuffle(players)
            count = 0
            msg=''
            for p in players:
                count = (count) % team_count
                teams[count].append(p)
                count+=1
            for t in range(0,len(teams)):
                msg+=f' **Team {(t+1)}** \n'
                for p in teams[t]:
                    msg+=f'{p}+\n'
                #msg+=f'{teams[t]} \n'
                print(msg)
            emb = discord.Embed(
                title="Teams",
                description=f'Dividing players into **{team_count}** teams',
                color=discord.Color.blurple())
            for t in range(0,len(teams)):
                msg=''
                for p in teams[t]:
                    msg+=f'{p} \n'
                emb.add_field(name=f'Team {(t+1)}', value=msg)
                print(msg)
            emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            #emb.set_footer(text=msg)
            await ctx.respond(embed=emb)
            print(teams)
            print(len(teams))


def setup(client):
    client.add_cog(Utils(client))
