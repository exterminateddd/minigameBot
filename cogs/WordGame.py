from discord.ext import commands
from discord import Embed, Message, errors
from classes.WordGameModel import WordGameModel, Word


class WordGame(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=['startWords', 'words', 'слова', 'начать_слова', 'начатьСлова'])
    @commands.has_permissions(ban_members=True)
    async def start_words(self, ctx: commands.Context, first_word: str = None):
        if not first_word:
            await ctx.send(f'Не указано первое слово!\nФормат команды: \n```{ctx.message.content.split(" ")[0]} [первое_слово]```')
            return
        ch = ctx.channel
        embed = Embed(title='Начало игры')
        embed.add_field(name='Игру начал @'+ctx.author.name, value='Вступайте в игру')
        await ctx.send(embed=embed)
        last_msg = await ctx.send('Первое слово: '+first_word)

        msg_count = 0
        game = WordGameModel(starter_id=ctx.author.id)

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

        while True:
            msg: Message = await self.bot.wait_for('message', check=lambda m: m.channel.id == ch.id)
            if msg.author.guild_permissions.ban_members and msg.content in ['КОНЕЦ', 'ЗАКОНЧИТЬ', 'END']:
                break
            try:
                if not await words_check(msg):
                    continue
                game.add_word(word=Word(word=msg.content, author_id=msg.author.id))
            except (commands.errors.CommandInvokeError, errors.NotFound):
                pass
            if ' ' in msg.content or not msg.content.isalpha():
                continue
            if msg.content[0] == last_msg.content[-1]:
                await ctx.send(f'{msg.author.mention} продолжает со словом {msg.content}')
                last_msg = msg
                msg_count += 1
        game.stop()
        end_embed = Embed(title='Конец игры')
        end_embed.add_field(name='Конечный счёт', value=str(msg_count), inline=False)
        end_embed.add_field(name='Победитель', value=last_msg.author.mention, inline=False)
        await ctx.send('', embed=end_embed)


def setup(bot: commands.Bot):
    bot.add_cog(WordGame(bot))
