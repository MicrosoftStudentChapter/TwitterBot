import discord
from discord.ext import commands, tasks
import random
import sqlite3
import csv

connection = sqlite3.connect('../twitterBot.db')
cursor = connection.cursor()


def random_six_digit_number_hex():
    return hex(random.randint(0, 8 ** 6))[2:]


class TechNews(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes=90)
    async def tech_validate(self):
        query = list(cursor.execute('''select * from News where SEEN = 0'''))
        ch = random.choice(seq=query)
        channel = self.client.get_channel(988184220327366746)  # TODO: Change in Production build
        news = await channel.send(
            embed=discord.Embed(title="How do you like this?", description=f"{ch[3]}\n [Here]({ch[4]})", ))
        cursor.execute('''UPDATE News SET SEEN = ? WHERE ID IS ?''', (str(news.id), ch[0]))
        connection.commit()
        await news.add_reaction('👍🏼')

    @commands.Cog.listener('on_raw_reaction_add')
    async def technews_add(self, payload):
        try:
            message_object = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        except discord.errors.NotFound:
            return
        if message_object.author.name in ['MLSC Bot'] and payload.member.bot is False:
            all_channel_ids = set(cursor.execute('''SELECT SEEN FROM NEWS;'''))
            if (message_object.id,) in all_channel_ids:
                cursor.execute('''UPDATE News SET IMPORTANCE = IMPORTANCE+100 WHERE SEEN IS ?''',
                               (str(message_object.id),))
                connection.commit()
            print('add ran')

    @commands.Cog.listener('on_raw_reaction_remove')
    async def technews_remove(self, payload):
        try:
            message_object = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        except discord.errors.NotFound:
            return
        if message_object.author.name in ['MLSC Bot']:
            all_channel_ids = set(cursor.execute('''SELECT SEEN FROM NEWS;'''))
            if (message_object.id,) in all_channel_ids:
                cursor.execute('''UPDATE News SET IMPORTANCE = IMPORTANCE-100 WHERE SEEN IS ?''',
                               (str(message_object.id),))
                connection.commit()
            print("remove ran")

    @commands.Cog.listener()
    async def on_ready(self):
        self.tech_validate.start()

    @commands.command(help="See the posts of this week")
    @commands.check_any(commands.has_permissions(ban_members=True), commands.is_owner())
    async def leaderboard(self, ctx):
        top10 = list(cursor.execute('''SELECT ID, TITLE, URL, IMPORTANCE FROM NEWS ORDER BY IMPORTANCE DESC;'''))
        file_pointer = open('temp.csv', 'w')
        writer = csv.writer(file_pointer)
        t = 1
        writer.writerow(["No.", "ID", "Title", "URL", "IMPORTANCE"])
        for item in top10:
            item = list(item)
            item.insert(0, t)
            t += 1
            writer.writerow(item)
        file_pointer.close()
        try:
            await ctx.message.author.send(file=discord.File('temp.csv'))
            await ctx.send("Shot you a DM!")
        except discord.errors.Forbidden:
            await ctx.send("Your DMs are closed")

    @commands.command(help="Add a user submission to the news\nWill always be displayed on the weekly tweet thread")
    @commands.check_any(commands.has_permissions(ban_members=True), commands.is_owner())
    async def add_news(self, ctx, title, url):
        cursor.execute('''INSERT INTO News (ID, SUBREDDIT, FLAIR, TITLE, URL) VALUES (?, "usersub", "usersubmission", ?, ?)''',
                       (random_six_digit_number_hex(), title, url))
        connection.commit()
        await ctx.send(embed=discord.Embed(title="Success", description="Added to the news"))


def setup(client):
    client.add_cog(TechNews(client))
