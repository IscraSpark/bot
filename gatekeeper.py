import os
import pathlib
import discord
from discord import utils
from discord.ext import commands
import config

from umongo import fields
from motor.motor_asyncio import AsyncIOMotorClient
from models import get_db


class GateKepeer(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("!help")
        await self.change_presence(status=discord.Status.online, activity=game)
        await self.setup()

    async def setup(self):
        path = pathlib.Path('cogs/')
        paths = list(path.rglob('*.py'))
        modules = [str(path).split("/")[-1].strip('.py') for path in paths]
        extensions = [f'cogs.{module}' for module in modules]
        print(extensions)

        for ext in extensions:
            await gk.load_extension(ext)


if __name__ == '__main__':
    intents = discord.Intents.all()
    intents.members = True

    # db = AsyncIOMotorClient(os.environ['MONGO_TOKEN'])['botbase']
    db = AsyncIOMotorClient(['MONGO_TOKEN'])['botbase']
    get_db(db)

    gk = GateKepeer(command_prefix="!", intents=intents)
    gk.remove_command('help')



    # gk.run(os.environ['DISCORD_TOKEN'])
    gk.run(config.TOKEN)
