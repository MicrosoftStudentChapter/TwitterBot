# import datetime
import re
import discord
from discord.ext import commands

from discord_bot import error_messages

TIME_REGEX = re.compile(r"(?:(\d{1,5})([hsmdw]))+?")
TIME_DICT = {"h": 3600, "s": 1, "m": 60, "d": 86400, "w": 604800}


def success():
    return discord.Embed(title="Your wish is my command", description="That was easy 😎")


def convert(argument):
    args = argument.lower()
    matches = re.findall(TIME_REGEX, args)
    time = 0
    for key, value in matches:
        try:
            time += TIME_DICT[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d|w are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Ban a member")
    @commands.check_any(commands.has_permissions(ban_members=True), commands.is_owner())
    async def ban(self, ctx, member: discord.Member, *, reason="exbo ki marzi"):
        if member == ctx.message.author:
            raise error_messages.YouMadeAMistake(value=member.display_name, message="You can't ban yourself")
        await member.ban(reason=reason)
        success_message = await ctx.send(embed=success())
        await success_message.add_reaction('✔')

    @commands.command(help="Unban a member")
    @commands.check_any(commands.has_permissions(ban_members=True), commands.is_owner())
    async def unban(self, ctx, member: discord.Member, *, reason="🎶 Everyone makes mistakes 🎶"):
        if member == ctx.message.author:
            raise error_messages.YouMadeAMistake(value=member.display_name,
                                                 message="You're trying to unban yourself...")
        await member.unban(reason=reason)
        success_message = await ctx.send(embed=success())
        await success_message.add_reaction('✔')

    @commands.command(help="Unban a member")
    @commands.check_any(commands.has_permissions(kick_members=True), commands.is_owner())
    async def kick(self, ctx, member: discord.Member, *, reason="🦵"):
        if member == ctx.message.author:
            raise error_messages.YouMadeAMistake(value=member.display_name,
                                                 message="You're trying to kick yourself...")
        await member.kick(reason=reason)
        success_message = await ctx.send(embed=success())
        await success_message.add_reaction('✔')

    # @commands.command(help='Give someone a Timeout (max 28 days)')
    # @commands.check_any(commands.has_permissions(kick_members=True), commands.is_owner())
    # async def timeout(self, ctx, member: discord.Member, duration: str = '1h', *, reason='bad boi'):  # TODO: Fix this
    #     if member == ctx.message.author:
    #         raise error_messages.YouMadeAMistake(value=member.display_name,
    #                                              message="Why do you think you have been a naughty boy 👄")
    #     if convert(duration) > 2419200 or convert(duration) < 0:
    #         raise error_messages.YouMadeAMistake(value=duration, message="Timeout can be between 1 second and 28 days")
    #     await member.timeout(until=datetime.timedelta(seconds=convert(duration)), reason=reason)
    #     success_message = await ctx.send(embed=success())
    #     await success_message.add_reaction('✔')

    @commands.command(help="Purge the Last `x` messages")
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def purge(self, ctx, number_messages: int = 10):
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=number_messages)
        success_message = await ctx.send(embed=success())
        await success_message.add_reaction('✔')

    @commands.command(help="Change someone's Nickname", alias=["nick"])
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def nickname(self, ctx, member: discord.Member, *, new_nick: str):
        await member.edit(nick=new_nick)
        success_message = await ctx.send(embed=success())
        await success_message.add_reaction('✔')

    @commands.command(help="Give someone a role")
    @commands.check_any(commands.has_permissions(manage_roles=True), commands.is_owner())
    async def add(self, ctx, member: discord.Member, role: discord.Role):
        if (role.position < ctx.author.top_role.position) or ctx.author.is_owner():
            await member.add_roles(role, reason=None, atomic=True)
            success_message = await ctx.send(embed=success())
            await success_message.add_reaction('✔')
        else:
            raise error_messages.YouMadeAMistake(value=role.name, message=f"Get on {member.display_name}'s level")

    @commands.command(help="Take a role from someone")
    @commands.check_any(commands.has_permissions(manage_roles=True), commands.is_owner())
    async def remove(self, ctx, member: discord.Member, role: discord.Role):
        if (role.position < ctx.author.top_role.position) or ctx.author.is_owner():
            await member.remove_roles(role, reason=None, atomic=True)
            success_message = await ctx.send(embed=success())
            await success_message.add_reaction('✔')
        else:
            raise error_messages.YouMadeAMistake(value=role.name, message=f"Get on {member.display_name}'s level")


def setup(client):
    client.add_cog(Moderation(client))
