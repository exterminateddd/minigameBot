from discord.ext import commands
from os import listdir
from loguru import logger
from discord import Intents
from utils import get_token

intents = Intents().default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


for filename in listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            logger.info('SUCCESSFULLY Loaded Module '+filename[:-3])
        except Exception as e:
            logger.error('FAILED to Load Module '+filename[:-3])
            raise e

bot.run(get_token())
