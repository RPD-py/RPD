from discord.ext.commands import Bot, Context
from discord.flags import Intents
from discord.ext.cogs import Cog
import sys
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("--token", "-t", type=str, required=True)
args = parser.parse_args()

intents = Intents.GUILD_MESSAGES | Intents.GUILDS | Intents.MESSAGE_CONTENT

bot = Bot(command_prefix='!', intents=intents, debug=True)


@bot.listen('on_ready')
async def on_ready():
    print(f'{bot.user} has logged in!')

@bot.command()
async def test(ctx):
    await ctx.send(f'pong! {round(bot.latency * 1000)}ms')

class Default(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.command()
    async def ping(self, ctx: Context):
        await ctx.send(f'pong! {round(self.bot.latency * 1000, 2)}ms')

bot.add_cog(Default(bot))
bot.run(args.token)