import discord
from discord.ext import commands, tasks
from discord_bot import error_messages
import random
import sqlite3
import csv

class MLSCPersonal(commands.Cog):
    def __init__(self, client):
        self.client = client

    #create a custom check for the commands which checks the server the command is run in
    def cog_check(self, ctx):
        return ctx.guild.id == 714456600043061248

    @commands.command(help = "Creates VC and Text chat for a new project", aliases = ["new"])
    @commands.check_any(commands.has_permissions(administrator=True))
    async def new_project(self,ctx ,name: str):
        category = discord.utils.get(ctx.guild.categories, name='project')
        channel = await ctx.guild.create_text_channel(name, category=category)
        await ctx.guild.create_voice_channel(name + "VC", category=category)
        #create a role
        role = await ctx.guild.create_role(name=name, colour=discord.Colour.random())
        await ctx.guild.edit_role_positions(positions={role: 7})

        await channel.send(f"Project {name} created! with role {role.mention}")




def setup(client):
    client.add_cog(MLSCPersonal(client))