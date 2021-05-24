from discord.ext import commands
from discord import Member, Embed, Message
from pytimeparse import parse
from classes.QuizGameModel import QuizGameModel

import asyncio


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=['quiz', 'startQuiz', 'viktorina', 'victorina'])
    async def start_quiz(self, ctx, n: int = 1, game_time: str = '5m'):
        try:
            parsed_time = parse(game_time)
        except TypeError:
            await ctx.send('Указанное время невалидно. Пример времени: `10m30s`')
            return
        ch = ctx.channel
        embed = Embed(title='Начало игры')
        embed.add_field(name='Викторину начал @'+ctx.author.name, value='Вступайте в игру')
        embed.add_field(name='Время игры', value=f'{game_time}')

        await ctx.send('', embed=embed)

        tried = []

        game = QuizGameModel(questions=n)

        async def end_callback(winner):
            embed = Embed()
            embed.add_field(name='Игра закончена!', value='=')
            embed.add_field(name='Победитель: ', value=winner.mention if winner else 'Никто не выиграл...')

        question = game.questions[game.current_question]

        last = question

        async def send_q_embed():
            q_embed = Embed()
            q_embed.add_field(name='Вопрос: ', value=game.questions[game.current_question]['question'])
            answers = game.questions[game.current_question]['answers']
            for i in range(len(answers)):
                q_embed.add_field(name=str(i+1), value=answers[i]['value'])
            await ctx.send('', embed=q_embed)

        await send_q_embed()

        async def loop():
            while True:
                msg: Message = await self.bot.wait_for('message', check=lambda m: m.channel.id == ch.id)
                if not msg.content.isalnum(): continue
                question = game.questions[game.current_question]

                if question != last:
                    await send_q_embed()

                if msg.author.id in tried:
                    await ctx.send(f'{msg.author.mention}, ты уже пробовал!')
                    continue
                tried.append(msg.author.id)
                if int(msg.content) > len(game.questions[game.current_question]):
                    await ctx.send(f'{msg.author.mention}, неправильный ответ!')
                if game.questions[game.current_question]['answers'].index([a for a in game.questions[game.current_question]['answers'] if a['right']][0]) == int(msg.content)-1:
                    await ctx.send(f'{msg.author.mention}, молодец! Правильный ответ!')
                    game.add_answer(msg.author)
                    tried.clear()
                    continue

        task = self.bot.loop.create_task(loop())

        done, pending = await asyncio.wait([task], return_when=asyncio.ALL_COMPLETED, timeout=parsed_time)
        print(task in done)
        if task in done:
            await end_callback(None)
        else:
            task.cancel()
            await end_callback(None)
        game.end()


def setup(bot: commands.Bot):
    bot.add_cog(Quiz(bot))
