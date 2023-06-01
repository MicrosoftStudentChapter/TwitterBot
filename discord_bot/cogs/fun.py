import datetime
from discord_bot import error_messages
import discord
import requests
from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(help="Get a random dog picture\nAccess: Everyone")
    async def dog(self, ctx):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Random Dog Picture",
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_image(url=data['message'])
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="dog",
                                                 message=f"There was an error getting a dog picture ({response.status_code})")

    @commands.command(help="Get a random fox picture\nAccess: Everyone")
    async def fox(self, ctx):
        response = requests.get("https://randomfox.ca/floof/")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Random Fox Picture",
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_image(url=data['image'])
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="fox",
                                                 message=f"There was an error getting a fox picture ({response.status_code})")

    @commands.command(help='Use the magic 8 ball to get a random answer\nAccess: Everyone', name='8ball')
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        await ctx.send(embed=discord.Embed(title="Magic 8 Ball",
                                           description=f'Question: {question}\nAnswer: {random.choice(responses)}',
                                           colour=discord.Colour.blurple()))

    @commands.command(help='Ask for a dare\nAccess: Everyone')
    async def dare(self, ctx):
        response = requests.get("https://api.truthordarebot.xyz/api/dare")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Random Dare",
                description=data['question'],
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="dare",
                                                 message=f"There was an error getting a dare ({response.status_code})")

    @commands.command(help='Ask for a truth\nAccess: Everyone')
    async def truth(self, ctx):
        response = requests.get("https://api.truthordarebot.xyz/v1/truth")

        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Random Truth",
                description=data['question'],
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="truth",
                                                 message=f"There was an error getting a truth ({response.status_code})")

    @commands.command(help="Translate to Yoda\nAccess: Everyone")
    async def yoda(self, ctx, *, text):
        response = requests.post("https://api.funtranslations.com/translate/yoda.json", data={"text": text})

        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Yoda Translator",
                description=f"Original:{data['contents']['text']}\nTranslated:{data['contents']['translated']}",
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url='https://images.immediate.co.uk/production/volatile/sites/3/2017/12/yoda-the'
                                    '-empire-strikes-back-28a7558.jpg?quality=90&resize=620,413')
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="yoda",
                                                 message=f"There was an error translating to Yoda ({response.status_code})")

    @commands.command(help='Get a Dad joke\nAccess: Everyone')
    async def dadjoke(self, ctx):
        response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
        if response.status_code == 200:
            data = response.json()
            await ctx.send(embed=discord.Embed(title="Dad Joke", description=data['joke']))
        else:
            raise error_messages.YouMadeAMistake(value="Dad",
                                                 message=f"There was an error getting a Dad Joke ({response.status_code})")

    @commands.command(help="Get Insulted by a piece of code\nAccess: Everyone")
    async def insult(self, ctx):
        response = requests.get("https://insult.mattbas.org/api/insult.json")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Insult",
                description=data['insult'],
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="insult",
                                                 message=f"There was an error getting an insult ({response.status_code})")

    @commands.command(help="Aur karo Computer Science\nAccess: Everyone")
    async def geek(self, ctx):
        response = requests.get("https://geek-jokes.sameerkumar.website/api")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Geek Time",
                description=data,
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="geek",
                                                 message=f"There was an error getting a Geeky joke ({response.status_code})")

    @commands.command(help="Get the twitter profile of MLSC, TIET\nAccess: Everyone")
    async def plug(self, ctx):
        embed = discord.Embed(
            title="MLSC Twitter",
            description="https://twitter.com/MLSC_TIET",
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
