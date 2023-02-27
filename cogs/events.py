from random import randint
from random import choice
import re
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from umongo import fields

import config
from gatekeeper import GateKepeer
from models import Note


class Events(commands.Cog):
    def __init__(self, bot: GateKepeer):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f'Member {member.name} left the server')
        if member.guild.id == 743742344511356938:
            channel = get(member.guild.text_channels, id=743742344955691130)
        else:
            try:
                channel = member.guild.system_channel
            except:
                channel = list(member.guild.text_channels)[0]
        left_emb = discord.Embed(title=f'{member.name} покинул сервер.',
                                 description=f'Пользователь {member.name} покинул сервер.',
                                 colour=discord.Color.dark_orange())
        await channel.send('', embed=left_emb)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == 743742344511356938:
            chanel = get(member.guild.text_channels, id=743742344955691130)
        else:
            try:
                chanel = member.guild.system_channel
            except:
                chanel = list(member.guild.text_channels)[0]

        greeting_emb = discord.Embed(colour=discord.Color.dark_orange())

        guild = member.guild
        emb_greeting = self.create_greeting(member, guild)
        if member.guild.id == 743742344511356938:
            role = guild.get_role(role_id=764177710326349834)
            await member.add_roles(role)
        await chanel.send(f'{member.mention}', embed=emb_greeting)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        channel = message.channel
        check = False
        for i in config.names:
            if i in message.content:
                check = True
        if check:
            check = False
            phrase = choice(config.phrases)
            await channel.send(f'{phrase}')

    @commands.command(name='note', aliases=('n',))
    async def note(self, ctx: commands.Context, *, data: str):
        note_name, note = data.split(':')
        note_d = Note(
            author_id=ctx.author.id,
            guild_id=ctx.guild.id,
            name=note_name,
            body=note,
        )
        await note_d.commit()
        await ctx.send(f'note created')

    @commands.command(name='notated', aliases=('nn',))
    async def notated(self, ctx: commands.Context):
        notes_ = Note.find({'guild_id': ctx.guild.id})
        count = await Note.count_documents()
        notes = await notes_.to_list(count)
        temp = ''
        for note in notes:
            temp = temp + note.name + ' '
        await ctx.send(f'{temp}')

    @commands.command(name='what', aliases=())
    async def what(self, ctx: commands.Context, *, data: str):
        note = await Note.find_one({'name': data, 'guild_id': ctx.guild.id})
        await ctx.send(f'{data}: {note.body}')

    @commands.command(name='dnote', aliases=('dn',))
    async def dnote(self, ctx: commands.Context, *, data: str):
        note = await Note.find_one({'name': data, 'guild_id': ctx.guild.id})
        if ctx.author.id == note.author_id or ctx.author.guild_permissions.manage_messages:
            await note.remove()
            await ctx.send(f'Note deleted {data}: {note.body}')
        else:
            await ctx.send(f'Похоже у вас недостаточно прав для выполнения данной команды')

    @commands.command(name='formula', aliases=('f',))
    async def formula(self, ctx: commands.Context, *, data: str):
        try:
            temp = ['__', 'lambda', 'import', 'os', 'system', 'clear']
            flag = False
            for i in temp:
                if i in data:
                    flag = True

            if not flag:
                res = eval(data, {'__builtins__': {}}, {})
            else:
                res = 'звучит странно, я не буду это выполнять'
        except:
            res = 'звучит странно, я не буду это выполнять'
        finally:
            await ctx.send(f'{res}')

    @staticmethod
    def create_greeting(member: discord.Member, guild: discord.Guild) -> discord.Embed:
        if member.guild.id == 743742344511356938:
            ch_rules = get(member.guild.text_channels, id=761539237937020929)
            me = guild.get_member(user_id=272013183927975936)
            template = {
                'title': f'Привет, {member.name}!\n',
                'description': f'Добро пожаловать на сервер, {member.mention}!\n'
                f'Предлагаю ознакомиться с правилами канала '
                f'{ch_rules.mention if ch_rules else "с правилами"},\n'
                f'обратись к {me.mention} чтобы получить роль'
            }
        else:
            template = {
                'title': f'Привет, {member.name}!\n',
                'description': f'Добро пожаловать на сервер, {member.mention}!\n'
            }

        greeting_emb = discord.Embed(title=template['title'], description=template['description'],
                                     colour=discord.Color.dark_orange())
        greeting_emb.set_thumbnail(url=member.avatar_url)

        return greeting_emb

    def roll(self, roll_w: str):
        dice_count, dice_means = roll_w.split('d')
        modifier = 0
        burst = False
        sort = False
        if 'b' in dice_count:
            burst = True
            b = dice_count.index('b')
            dice_count = dice_count[b+1:]
        if 's' in dice_count:
            sort = True
            s = dice_count.index('s')
            dice_count = dice_count[s + 1:]
        if 'mm' in dice_means:
            dice_means, mean = dice_means.split('mm')
            modifier = -int(mean)
        if 'm' in dice_means:
            dice_means, mean = dice_means.split('m')
            modifier = int(mean)
        if '_' in roll_w:

            if not dice_count:
                dice_count = 1

            dice_max, dice_min = dice_means.split('_')
            if dice_min == dice_max:
                burst = False
            result = [randint(int(dice_min), int(dice_max)) + modifier for _ in range(int(dice_count))]
            dice_means = dice_max
        else:
            if int(dice_means) == 1:
                burst = False
            if not dice_count:
                dice_count = 1

            result = [randint(1, int(dice_means)) + modifier for _ in range(int(dice_count))]

        bursted = result.count(int(dice_means) + modifier)
        if burst and bursted:
            new_roll = 'b' + str(bursted) + 'd' + str(dice_means)
            temp = self.roll(new_roll)
            result = result + temp

        if sort:
            result.sort(reverse=True)

        return result

    @staticmethod
    def get_delay(delay_str: str):
        res = re.findall(r'\d+d|\d+h|\d+m|\d+s|\d+д|\d+ч|\d+м|\d+с', delay_str)

        if ''.join(res) != delay_str:
            return 'звучит странно, я не буду это выполнять'

        delay_dict = {'d': 86400, 'h': 3600, 'm': 60, 's': 1,
                      'д': 86400, 'ч': 3600, 'м': 60, 'с': 1, }

        delay = 0
        for r in res:
            delay += int(r[:-1]) * delay_dict[r[-1]]

        return delay

    @commands.command(name='timer', aliases=('t', 'таймер', 'т'))
    async def timer(self, ctx: commands.Context, *, time: str):
        delay = self.get_delay(time)
        if delay == 'звучит странно, я не буду это выполнять':
            await ctx.send(f'{delay}')
        else:
            await ctx.send(f'таймер создан')
            await asyncio.sleep(delay)
            await ctx.send(f'{ctx.author.name}, время вышло')

    @commands.command(name='rroll', aliases=('r', 'р', 'к'))
    async def r_roll(self, ctx: commands.Context, *, dices: str):
        dices = re.sub(r'[дв]', 'd', dices)
        result = self.roll(dices)
        await ctx.send(f'{ctx.author.name} roll: {result}: {sum(result)}')

    @commands.command(name='croll', aliases=('cr', 'ск'))
    async def c_roll(self, ctx: commands.Context, *, dices: str):
        try:
            temp = ['__', 'lambda', 'import', 'os', 'system', 'clear']
            flag = False
            for i in temp:
                if i in dices:
                    flag = True

            if not flag:
                data = re.sub(r'[дв]', 'd', dices)
                operands = re.split(r'\W', data)
                # print(operands)
                for i in range(len(operands)):
                    if 'd' in operands[i]:
                        data = data.replace(operands[i], str(sum(self.roll(operands[i]))), 1)
                # print(data)
                res = eval(data, {'__builtins__': {}}, {})
            else:
                res = 'звучит странно, я не буду это выполнять'
        except:
            res = 'звучит странно, я не буду это выполнять'
        finally:
            await ctx.send(f'{ctx.author.name} roll: {res}')

    @commands.command(name='del', aliases=('delete', ))
    @commands.has_permissions(manage_messages=True)
    async def delete_mess(self, ctx: commands.Context, *, param: str):
        await ctx.channel.purge(limit=int(param)+1)
        await ctx.channel.send(f'{ctx.author.name} deleted {param} message(s)')

    @delete_mess.error
    async def delete_mess_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Похоже у вас недостаточно прав для выполнения данной команды")

    @commands.command(name='coin', aliases=('монетка',))
    async def coin(self, ctx: commands.Context):
        num = randint(1, 1000)

        if num in range(1, 496):
            answer = f'Орел'
        elif num in range(496, 506):
            answer = f'Ребро'
        else:
            answer = f'Решка'

        await ctx.send(answer)

    @commands.command(name='help', aliases=())
    async def help(self, ctx: commands.Context):
        command = config.COMMANDS.keys()
        template = ''
        for i in command:
            template = template + i + ':' + config.COMMANDS[i] + '\n'

        emb = discord.Embed(title='Список команд', description=template,
                            colour=discord.Color.dark_orange())
        await ctx.send('', embed=emb)

    @commands.command(name='say', aliases=('скажи',))
    async def say(self, ctx: commands.Context, *, text: str):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(name='choose', aliases=('выбрать', 'выбери'))
    async def choose(self, ctx: commands.Context, *options):
        opt = choice(options)
        await ctx.send(opt)


async def setup(bot: GateKepeer):
    await bot.add_cog(Events(bot))
