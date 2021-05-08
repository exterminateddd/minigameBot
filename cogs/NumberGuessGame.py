from discord.ext import commands
from discord import Embed, Message, errors
from random import randint
from classes.NumberGameModel import NumberGameModel
from classes.Number import Number


class NumberGuessGame(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=['guess', 'startGuess', 'guessNum', 'guessnum', 'угадайчисло'])
    async def start_guess_num(self, ctx, max_num: int = 10):
        embed = Embed(title='Начало игры')
        embed.add_field(name='Игру начал @' + ctx.author.name, value='Вступайте в игру')
        embed.add_field(name='Промежуток чисел', value=f'0 - {max_num}')
        await ctx.send('', embed=embed)

        game = NumberGameModel(starter_id=ctx.author.id, max_num=max_num)
        msg_count = 0
        last_msg: Message

        async def number_check(m: Message):
            if str(m.content).isalnum():
                return True
            await m.delete()

        async def has_tried(user_id):
            return user_id in [i['author_id'] for i in game.data['numbers']]

        while True:
            msg: Message = await self.bot.wait_for('message', check=lambda m: m.channel.id == ctx.channel.id)
            if msg.author.guild_permissions.ban_members and msg.content in ['КОНЕЦ', 'ЗАКОНЧИТЬ', 'END']:
                break
            if ' ' in msg.content or await has_tried(int(msg.author.id)):
                await msg.delete()
                continue
            try:
                if not await number_check(msg):
                    continue
                last_msg = msg
                msg_count += 1
                game.add_num(num=Number(number=msg.content, author_id=msg.author.id))
            except (commands.errors.CommandInvokeError, errors.NotFound):
                pass
            if str(msg.content) == str(game.actual):
                game.stop(msg.author.id)
                break
        end_embed = Embed(title='Конец игры')
        end_embed.add_field(name='Попыток', value=str(msg_count), inline=False)
        end_embed.add_field(name='Ответ', value=str(game.actual), inline=False)
        end_embed.add_field(name='Победитель', value=last_msg.author.mention, inline=False)
        await ctx.send('', embed=end_embed)


def setup(bot: commands.Bot):
    bot.add_cog(NumberGuessGame(bot))
