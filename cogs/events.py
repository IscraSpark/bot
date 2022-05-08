from random import randint
from random import choice
import discord
from discord.ext import commands
from discord.utils import get
import config
from gatekeeper import GateKepeer


class Events(commands.Cog):
    def __init__(self, bot: GateKepeer):
        self.bot = bot
        self.notates = {}

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f'Member {member.name} left the server')

        channel = get(member.guild.text_channels, id=743742344955691130)
        await channel.send(f'Пользователь {member.name} покинул сервер.')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        chanel = get(member.guild.text_channels, id=743742344955691130)

        greeting_emb = discord.Embed(colour=discord.Color.dark_orange())

        guild = member.guild
        emb_greeting = self.create_greeting(member, guild)

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
        self.notates[note_name] = note
        await ctx.send(f'note created')

    @commands.command(name='notated', aliases=('nn',))
    async def noteated(self, ctx: commands.Context):
        notes = self.notates.keys()
        temp = ''
        for note_names in notes:
            temp = temp + note_names + ', '
        await ctx.send(f'{temp}')

    @commands.command(name='what', aliases=())
    async def what(self, ctx: commands.Context, *, data: str):
        await ctx.send(f'{data}: {self.notates[data]}')

    @staticmethod
    def create_greeting(member: discord.Member, guild: discord.Guild) -> discord.Embed:
        ch_rules = get(member.guild.text_channels, id=761539237937020929)
        me = guild.get_member(user_id=272013183927975936)
        template = {
            'title': f'Привет, {member.name}!\n',
            'description': f'Добро пожаловать на сервер, {member.mention}!\n'
            f'Предлагаю ознакомиться с правилами канала '
            f'{ch_rules.mention if ch_rules else "с правилами"},\n'
            f'обратись к {me.mention} чтобы получить роль'
        }

        greeting_emb = discord.Embed(title=template['title'], description=template['description'],
                                     colour=discord.Color.dark_orange())
        greeting_emb.set_thumbnail(url=member.avatar_url)

        return greeting_emb

    @commands.command(name='rroll', aliases=('r', 'р', 'к'))
    async def r_roll(self, ctx: commands.Context, *, dices: str):
        dice_count, dice_means = dices.split('d')
        if not dice_count:
            dice_count = 1

        result = [randint(1, int(dice_means)) for _ in range(int(dice_count))]

        await ctx.send(f'{ctx.author.name} roll: {result}: {sum(result)}')

    @commands.command(name='croll', aliases=('cr', 'ск'))
    async def c_roll(self, ctx: commands.Context, *, dices: str):
        dice_count, dice_means = dices.split('d')
        if not dice_count:
            dice_count = 1

        dice_max, dice_min = dice_means.split('_')
        result = [randint(int(dice_min), int(dice_max)) for _ in range(int(dice_count))]
        await ctx.send(f'{ctx.author.name} roll: {result}: {sum(result)}')

    @commands.command(name='del', aliases=())
    async def delete_mess(self, ctx: commands.Context, *, param: str):
        await ctx.channel.purge(limit=int(param)+1)
        await ctx.channel.send(f'Deleted {param} message(s)')

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
        await ctx.send(template)

    @commands.command(name='say', aliases=('скажи',))
    async def say(self, ctx: commands.Context, *, text: str):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(name='choose', aliases=('выбрать', 'выбери'))
    async def choose(self, ctx: commands.Context, *options):
        opt = choice(options)
        await ctx.send(opt)


def setup(bot: GateKepeer):
    bot.add_cog(Events(bot))
