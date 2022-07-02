import datetime
import discord
from discord.ext import commands

from discord_bot import error_messages

# TIME_REGEX = re.compile(r"(?:(\d{1,5})([hsmdw]))+?")
# TIME_DICT = {"h": 3600, "s": 1, "m": 60, "d": 86400, "w": 604800}
NUM_DICT = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

def success():
    return discord.Embed(title="Your wish is my command", description="That was easy 😎")


# def convert(argument):
#     args = argument.lower()
#     matches = re.findall(TIME_REGEX, args)
#     time = 0
#     for key, value in matches:
#         try:
#             time += TIME_DICT[value] * float(key)
#         except KeyError:
#             raise commands.BadArgument(
#                 f"{value} is an invalid time key! h|m|s|d|w are valid arguments"
#             )
#         except ValueError:
#             raise commands.BadArgument(f"{key} is not a number!")
#     return round(time)


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
    # @commands.check_any(commands.has_permissions(
    # kick_members=True), commands.is_owner()) async def timeout(self, ctx, member: discord.Member, duration: str =
    # '1h', *, reason='bad boi'):  // Fix this if member == ctx.message.author: raise
    #  error_messages.YouMadeAMistake(value=member.display_name, message="Why do you think you have been a naughty
    #  boy 👄") if convert(duration) > 2419200 or convert(duration) < 0: raise error_messages.YouMadeAMistake(
    #  value=duration, message="Timeout can be between 1 second and 28 days") await member.timeout(
    #  until=datetime.timedelta(seconds=convert(duration)), reason=reason) success_message = await ctx.send(
    #  embed=success()) await success_message.add_reaction('✔')

    @commands.command(help="Purge the Last `x` messages")
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def purge(self, ctx, number_messages: int = 10):
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=number_messages)
        success_message = await ctx.send(embed=success())
        await success_message.add_reaction('✔')

    @commands.command(help="Purge all messages from a user")
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def purge_user(self, ctx, member: discord.Member, number_messages: int = 150):
        passed_before = ctx.message

        await ctx.channel.purge(limit=number_messages, before=passed_before, check=lambda m: (m.author == member and m.created_at >= passed_before.created_at - datetime.timedelta(days=2)))

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

    @commands.command(help="Create a Poll")
    async def poll(self, ctx, question: str, *options):
        if len(options) < 2:
            raise error_messages.YouMadeAMistake(value=options, message="You need at least 2 options")
        if len(options) >= 10:
            raise error_messages.YouMadeAMistake(value=options, message="You can't have more than 10 options")
        if len(question) > 200:
            raise error_messages.YouMadeAMistake(value=question, message="Your question is too long")
        if len(options) > 1:
            embed = discord.Embed(title=question, color=0x00ff00)
            for i in range(len(options)):
                embed.add_field(name=f"{NUM_DICT[i]} - {options[i]}", value="‎", inline=True)
            msg = await ctx.send(embed=embed)
            for i in range(len(options)):
                await msg.add_reaction(NUM_DICT[i])
        else:
            raise error_messages.YouMadeAMistake(value=options, message="You need at least 2 options")


def setup(client):
    client.add_cog(Moderation(client))
