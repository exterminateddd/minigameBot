from discord.ext import commands
from discord import Embed, Message, errors
from classes.WordGameModel import WordGameModel, Word
from asyncio import wait
from pytimeparse import parse
from utils import *

import asyncio


class WordGame(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=['startWords', 'words', 'слова', 'начать_слова', 'начатьСлова', 'города', 'cities'])
    @commands.has_permissions(ban_members=True)
    async def start_words(self, ctx: commands.Context, first_word: str = None, game_time: str = '5m'):
        try:
            parsed_time = parse(game_time)
        except TypeError:
            await ctx.send('Указанное время невалидно. Пример времени: `10m30s`')
            return
        if not first_word:
            await ctx.send(
                f'Не указано первое слово!\nФормат команды: \n```{ctx.message.content.split(" ")[0]} [первое_слово]```'
            )
            return
        ch = ctx.channel
        embed = Embed(title='Начало игры')
        embed.add_field(name='Игру начал @'+ctx.author.name, value='Вступайте в игру')
        embed.add_field(name='Время игры', value=f'{game_time}')
        await ctx.send(embed=embed)
        last_msg = await ctx.send('Первое слово: '+first_word)

        msg_count = 0
        game = WordGameModel(starter_id=ctx.author.id)

        data = {
            "last_msg": last_msg,
            "count": msg_count
        }

        async def end_callback(winner=None, count=0):
            end_embed = Embed(title='Конец игры')
            end_embed.add_field(name='Конечный счёт', value=str(count), inline=False)
            if winner:
                end_embed.add_field(name='Победитель', value=winner.mention, inline=False)
            await ctx.send('', embed=end_embed)

        async def words_check(m: Message):
            if msg_count <= 1: return True
            if m.channel.id == ch.id:
                if m.author.id != last_msg.author.id:
                    return True
                else:
                    await ctx.send('Не твоя очередь!')
            else:
                pass
                # await m.delete()

        async def loop(fin_msg):

            while True:
                msg: Message = await self.bot.wait_for('message', check=lambda m: m.channel.id == ch.id)
                if msg.author.bot: continue
                if msg.author.guild_permissions.ban_members and msg.content in ['КОНЕЦ', 'ЗАКОНЧИТЬ', 'END']:
                    break
                try:
                    if not await words_check(msg):
                        continue
                    game.add_word(word=Word(word=msg.content, author_id=msg.author.id))
                except (commands.errors.CommandInvokeError, errors.NotFound):
                    pass
                if data['last_msg'].author.id == msg.author.id:
                    await ctx.send(f'{msg.author.mention}, не твоя очередь!')
                    continue
                if ' ' in msg.content or not msg.content.isalpha():
                    continue
                if msg.content[0] != data['last_msg'].content[-1] or not is_city_valid(msg.content.lower()):
                    await ctx.send(f'{msg.author.mention}, слово не подходит / не является названием города!')
                else:
                    await ctx.send(f'{msg.author.mention} продолжает со словом {msg.content}')
                    data['count'] += 1
                    data['last_msg'] = msg

        task = self.bot.loop.create_task(loop(data['last_msg']))

        done, pending = await asyncio.wait([task], return_when=asyncio.ALL_COMPLETED, timeout=parsed_time)
        print(task in done)
        if task in done:
            await end_callback(None)
        else:
            task.cancel()
            await end_callback(data['last_msg'].author, data['count'])
        game.stop()


def setup(bot: commands.Bot):
    bot.add_cog(WordGame(bot))
