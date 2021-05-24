from discord.ext import commands
from discord import Member, Embed, Colour
from utils import *


class GameStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['победы', 'wins', 'stat', 'stats', 'стат'])
    async def get_wins(self, ctx, user: Member):
        embed = Embed(title=f'Победы {user.mention}')
        embed.add_field(name='Слова', value=str(get_words_count(str(user.id))))
        embed.add_field(name='Угадай число', value=str(get_num_wins(str(user.id))))
        embed.add_field(name='Викторина', value=str(get_quiz_wins(str(user.id))))
        await ctx.send('', embed=embed)

    @commands.command()
    async def top_num(self, ctx):
        embed = Embed(title='ТОП по игре "Угадай Число"', colour=Colour.gold())
        wins = {
            f'@{m.display_name}#{m.discriminator}': get_num_wins(m.id) for m in await ctx.guild.fetch_members().flatten() if get_num_wins(m.id) != 0
        }
        for k, v in wins.items():
            print(k, v)
            embed.add_field(name=f'{k}', value=str(v))
        await ctx.send('', embed=embed)

    @commands.command()
    async def top_words(self, ctx):
        embed = Embed(title='ТОП по игре "Слова"', colour=Colour.gold())
        wins = {
            f'@{m.display_name}#{m.discriminator}': get_word_wins(m.id) for m in await ctx.guild.fetch_members().flatten() if get_word_wins(m.id) != 0
        }
        for k, v in wins.items():
            print(k, v)
            embed.add_field(name=f'{k}', value=str(v))
        await ctx.send('', embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(GameStats(bot))
