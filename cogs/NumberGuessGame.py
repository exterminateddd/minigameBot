from discord.ext import commands
from discord import Embed, Message, errors
from classes.NumberGameModel import NumberGameModel
from classes.Number import Number
from pytimeparse import parse
from time import time

import threading
import asyncio


game_run: bool = True


async def timer(ctx, delay):
    global game_run
    cur_time = int(time())

    for _ in range(delay):
        await asyncio.sleep(1)
    await ctx.send('game ended')
    game_run = False


class NumberGuessGame(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=['guess', 'startGuess', 'guessNum', 'guessnum', 'угадайчисло'])
    async def start_guess_num(self, ctx, max_num: int = 10, game_time: str = None):
        parsed_time = None
        try:
            if game_time:
                parsed_time = parse(game_time)
        except KeyError:
            await ctx.send('Указанное время невалидно. Пример времени: `10m30s`')
            return
        embed = Embed(title='Начало игры')
        embed.add_field(name='Игру начал @' + ctx.author.name, value='Вступайте в игру', inline=False)
        embed.add_field(name='Промежуток чисел', value=f'0 - {max_num}', inline=False)

        game = NumberGameModel(starter_id=ctx.author.id, max_num=max_num)
        msg_count = 0
        last_msg: Message

        async def end_callback(winner=None):
            end_embed = Embed(title='Конец игры')
            end_embed.add_field(name='Попыток', value=str(msg_count), inline=False)
            end_embed.add_field(name='Ответ', value=str(game.actual), inline=False)
            if winner:
                end_embed.add_field(name='Победитель', value=winner.mention, inline=False)
            else:
                end_embed.add_field(name='Никто не выиграл', value='=(', inline=False)
            await ctx.send('', embed=end_embed)

        if game_time:
            embed.add_field(name='Время игры', value=f'{game_time}', inline=False)

        await ctx.send('', embed=embed)

        async def number_check(m: Message):
            if str(m.content).isalnum():
                return True

        async def has_tried(user_id):
            return user_id in [i['author_id'] for i in game.data['numbers']]

        cur_time = int(time())
        broken = False
        last_msg = ctx.message

        async def loop():
            global msg_count
            global broken
            global last_msg
            broken = False
            msg_count = 0
            while game_run:
                msg: Message = await self.bot.wait_for('message', check=lambda m: m.channel.id == ctx.channel.id)
                if msg.author.bot: continue
                if msg.author.guild_permissions.ban_members and msg.content in ['КОНЕЦ', 'ЗАКОНЧИТЬ', 'END']:
                    broken = True
                    break
                if not msg:
                    if int(time()) - cur_time >= parsed_time:
                        game.stop(0)
                        await end_callback()
                        return
                if await has_tried(int(msg.author.id)):
                    await ctx.send(f'{msg.author.mention}, ты уже пробовал!')
                    continue
                msg_count += 1
                try:
                    if not await number_check(msg):
                        continue
                    last_msg = msg
                    game.add_num(num=Number(number=msg.content, author_id=msg.author.id))
                except (commands.errors.CommandInvokeError, errors.NotFound):
                    pass
                if str(msg.content) == str(game.actual):
                    game.stop(msg.author.id)
                    await end_callback(msg.author)
                    return
                else:
                    await ctx.send(f'{msg.author.mention}, неправильно!')

        task = self.bot.loop.create_task(loop())

        done, pending = await asyncio.wait([task], return_when=asyncio.ALL_COMPLETED, timeout=parsed_time)
        print(task in done)
        if task not in done:
            game.stop(last_msg.author.id)
            await end_callback(None)


def setup(bot: commands.Bot):
    bot.add_cog(NumberGuessGame(bot))
