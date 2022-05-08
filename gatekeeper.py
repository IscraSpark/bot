import os
import pathlib
import discord
from discord import utils
from discord.ext import commands
import config


class GateKepeer(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("!help")
        await self.change_presence(status=discord.Status.online, activity=game)


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True

    gk = GateKepeer(command_prefix="!", intents=intents)
    gk.remove_command('help')

    path = pathlib.Path('cogs/')
    paths = list(path.rglob('*.py'))
    modules = [str(path).split("/")[-1].strip('.py') for path in paths]
    extensions = [f'cogs.{module}' for module in modules]
    print(extensions)

    for ext in extensions:
        gk.load_extension(ext)

    # gk.run(os.environ['DISCORD_TOKEN'])
    gk.run(config.TOKEN)