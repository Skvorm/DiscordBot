import random
from discord.ext import commands
from BotHelperFunctions import get_roll_range




class Roll(commands.Cog, name="Roll"):
    def __init__(self, client):
        self.client = client

    desc = "gets a Random Number"
    help_long = "Can be used to get a random number within a set range or to emulate a dice roll \
    with variable number of dice and number of sides\nExample:\n!roll 1-100 (rolls between 1-100)\n\
    !roll 3d6   (rolls 3 6-sided dice)\n!roll 1d20  (rolls 1 20-sided die)"
    help_brief = "generates a random number or a dice roll"

    @commands.command(name="roll",description=desc,help=help_long,brief=help_brief)
    async def roll(self, ctx):
        try:
            rng = get_roll_range(str(ctx.message.content))
        except ValueError:
            # default value of range(1-00), and 1 die
            rng = [1, 100, 1]

        if rng[2] > 1:
            vals = []
            total = 0
            for i in range(0, int(rng[2])):
                roll_val = random.randint(rng[0], rng[1])
                vals.append(roll_val)
                total += roll_val
            roll_val = random.randint(rng[0], rng[1])
            if len(vals) <= 50:
                str_v = str(vals)
                msg = f"**({str(rng[2])}d{str(rng[1])})**: {str(ctx.author.name)} rolled **{str(total)}**: {str_v}"
            else:
                msg = f"**({str(rng[2])}d{str(rng[1])})**: {str(ctx.author.name)} rolled **{str(total)}**"
        else:
            roll_val = random.randint(rng[0], rng[1])
            msg = f"**({str(rng[0])}, {str(rng[1])})**: {str(ctx.author.name)} rolled **{str(roll_val)}**"
        await ctx.send(msg)


def setup(client):
    client.add_cog(Roll(client))
