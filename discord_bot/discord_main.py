import contextlib
import io
import discord
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import sqlite3
import textwrap
import traceback
import time
import os


# ----------
load_dotenv('../.env')


def cleancode(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


def success(title: str = "Your wish is my command", description: str = "That was easy 😎"):
    return discord.Embed(title=title, description=description, colour=discord.Colour.green())


def get_prefix(client, message):
    with open('prefix.txt', 'r') as file:
        return file.readline()[0]

# ----------


class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    def get_ending_note(self):
        command_name = self.invoked_with
        return "Type {0}{1} <command/category> for more information | [Optional Arg], <Required Arg>".format(self.clean_prefix, command_name)

    async def send_bot_help(self, mapping):
        help_command = discord.Embed(
            title='Help is on the way',
            description=f'Heard you needed help! Here are all the commands you can access. {client.description}',
            colour=discord.Colour.blurple(),

        )
        for cog in mapping:
            if cog is not None:
                cog_name = cog.qualified_name
            else:
                cog_name = 'Normie Commands'
            filtered = await self.filter_commands([command for command in mapping[cog]])
            value = os.linesep.join([("> " + command.name.title()) for command in filtered])
            if len(value) > 1:
                help_command.add_field(name=cog_name, value=value)

        help_command.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=help_command)
        return await super(CustomHelpCommand, self).send_bot_help(mapping)

    async def send_cog_help(self, cog):
        cog_embed = discord.Embed(
            title=cog.qualified_name,
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        filtered = await self.filter_commands([command for command in cog.get_commands()], sort=True)
        for command in filtered:
            cog_embed.add_field(name=command.name.title(), value=command.help, inline=False)
        cog_embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=cog_embed)
        return await super(CustomHelpCommand, self).send_cog_help(cog)

    async def send_group_help(self, group):  # Don't Need
        return await super(CustomHelpCommand, self).send_group_help(group)

    async def send_command_help(self, command):
        ctx = self.context
        if len("|".join(command.aliases)) > 0:
            base = f'{get_prefix(client, ctx.message)}[{command.name}|{"|".join(command.aliases)}]'
        else:
            base = f'{get_prefix(client, ctx.message)}[{command.name}]'
        syntax = f'```{base} {command.signature}```'
        command_embed = discord.Embed(
            title=command.name.title(),
            description=command.help + '\n' + syntax,
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        command_embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=command_embed)
        return await super(CustomHelpCommand, self).send_command_help(command)


# ----------


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True,
                      help_command=CustomHelpCommand())

# ----------

connection = sqlite3.connect('../twitterBot.db')
cursor = connection.cursor()


# ----------


@client.event
async def on_ready():
    cog_list = [cog.replace('.py', '' ) for cog in os.listdir('./cogs') if cog.endswith('.py')]
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="over the server"))
    print('Bot is ready')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cogs(name VARCHAR(20) PRIMARY KEY, toggle BIT(1));''')  # table schema
    connection.commit()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS News(ID VARCHAR(10) PRIMARY KEY, SUBREDDIT VARCHAR(50), FLAIR VARCHAR(50), 
        TITLE VARCHAR(500) UNIQUE, URL VARCHAR(255) UNIQUE, RATIO FLOAT, SCORE INT, TOTALCOMMENTS INT, IMPORTANCE INT, SEEN BITINT);''')  # table schema
    connection.commit()
    query = list(cursor.execute('''SELECT * FROM COGS'''))
    cog_list_query = [cog[0] for cog in query]
    for cog in cog_list:
        if cog not in cog_list_query:
            cursor.execute('''INSERT INTO COGS VALUES(?, ?)''', (cog, 1))
            connection.commit()
    query = list(cursor.execute('''SELECT * FROM COGS'''))
    for cog in query:
        if cog[1] == 1:
            try:
                client.load_extension(f'cogs.{cog[0]}')
            except commands.ExtensionAlreadyLoaded:
                pass
        else:
            client.unload_extension(f'cogs.{cog[0]}')


@client.command(help='Get Bot and Database Latency\nAccess: Everyone')
@commands.check_any(commands.has_role('Staff'), commands.is_owner())
async def ping(ctx):
    bot_latency = str((round(client.latency * 1000, 2))) + ' ms'
    await ctx.send(
        embed=discord.Embed(title="Ping Check", description=f"The Bot ping is {bot_latency * 1000} ms"))


@client.command(help='Enables Different Categories\nAccess: Administrator')
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def enable(ctx, extension: str):
    client.load_extension(f'cogs.{extension.lower()}')
    cursor.execute('''UPDATE COGS SET TOGGLE = 1 WHERE NAME IS ?;''', (extension.lower(),))
    connection.commit()
    success_message = await ctx.send(embed=success())
    await success_message.add_reaction('✔')


@client.command(help='Disables Different Categories\nAccess: Administrator')
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def disable(ctx, extension: str):
    client.unload_extension(f'cogs.{extension.lower()}')
    cursor.execute('''UPDATE COGS SET TOGGLE = 0 WHERE NAME IS ?;''', (extension.lower(),))
    connection.commit()
    success_message = await ctx.send(embed=success())
    await success_message.add_reaction('✔')


@client.command(aliases=['eval'], help='Run a snippet of code\nAccess: Bot Owner')
@commands.is_owner()
async def code(ctx, *, block):
    code_block = cleancode(block)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "client": client,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
    }

    stdout = io.StringIO()
    start_time = time.time() * 1000
    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code_block, '    ')}", local_variables,
            )
            await ctx.message.add_reaction("🔃")
            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}"
            react_add = '✅'
    except Exception as e:
        # noinspection PyTypeChecker
        result = "".join(traceback.format_exception(e, e, e.__traceback__))  # This error is okay
        obj = e
        react_add = '❌'
    end_time = time.time() * 1000
    await ctx.message.remove_reaction("🔃", client.user)
    await ctx.send(f'```py\n{result}\n[{obj}]\nExecuted in {round(end_time - start_time, 3)} ms```')
    await ctx.message.add_reaction(react_add)


@client.command(help='Changes Current prefix\nAccess: Administrator')
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def prefix(ctx, new_prefix=None):
    if new_prefix is None:
        await ctx.send(f'Server prefix is **{get_prefix(client, ctx.message)}**')
    else:
        new_prefix = new_prefix.strip()
        if len(new_prefix) > 0:

            with open('prefix.txt', 'w') as file:
                file.writelines(new_prefix)
            await ctx.send(f'Changed server prefix to "**{new_prefix}**"')
        else:
            raise BrokenPipeError("Only Invisible Character prefix aren't allowed")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        if len("|".join(ctx.command.aliases)) > 0:
            base = f'{get_prefix(client, ctx.message)}[{ctx.command.name}|{"|".join(ctx.command.aliases)}]'
        else:
            base = f'{get_prefix(client, ctx.message)}[{ctx.command.name}]'
        error = f'{str(error)}\nCorrect syntax: ```{base} {ctx.command.signature}```'
    else:
        if str(error).startswith("Command"):
            error = str(error)[29:]
        else:
            error = str(error)
    embed = discord.Embed(
        title="This isn't a 404 but...",
        description=error,
        colour=discord.Colour(0xE93316)
    )
    embed.set_footer(text=f'For more information try running {get_prefix(client, ctx.message)}help')

    await ctx.message.channel.send(embed=embed)


# ----------
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")
# ----------
client.run(str(os.getenv('DISCORD_TOKEN')))
