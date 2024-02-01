import disnake
from disnake.ext import commands
import os

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents, test_guilds=[1022510823282851961])
bot.remove_command('help')


class Member:
    def __init__(self, id, roles):
        self.id = id
        self.roles = roles
        self.roles_ids = [role.id for role in roles]


@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Game('Версия 1.2'))
    for guild in bot.guilds:
        for member in guild.members:
            member_obj = Member(member.id, member.roles)
            member = member_obj
    print('BOT CONNECTED')


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run('YOUR TOKEN')
