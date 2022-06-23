import datetime
from discord_bot import error_messages
import discord
import requests
from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Get a random cat picture")
    async def cat(self, ctx):
        response = requests.get("https://aws.random.cat/meow")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Random Cat Picture",
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_image(url=data['file'])
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="cat",
                                                 message=f"There was an error getting a cat picture ({response.status_code})")

    @commands.command(help="Get a random dog picture")
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

    @commands.command(help="Get a random fox picture")
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

    @commands.command(help='Use the magic 8 ball to get a random answer', aliases=['8ball'])
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

    @commands.command(help='Ask for a dare')
    async def dare(self, ctx):
        response = requests.get("https://api.truthordarebot.xyz/api/dare")
        print(response.json())
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

    @commands.command(help='Ask for a truth')
    async def truth(self, ctx):
        response = requests.get("https://api.truthordarebot.xyz/v1/truth")
        print(response.json())
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

    @commands.command(help='Ask for a pickup line')
    async def pickup(self, ctx):
        response = requests.get("https://getpickuplines.herokuapp.com/lines/random")
        print(response.json())
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Random Pickup Line",
                description=data['line'],
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="pickup",
                                                 message=f"There was an error getting a pickup line ({response.status_code})")

    @commands.command(help="How old does the bot think you are?")
    async def oldie(self, ctx, name: str):
        response = requests.get(f"https://api.agify.io/?name={name}")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title=f"How old is {name}?",
                description=f"According to Agify, {name} is {data['age']} years old.",
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="oldie",
                                                 message=f"There was an error getting the age of the user ({response.status_code})")

    @commands.command(help="Get a Kanye West quote")
    async def kanye(self, ctx):
        response = requests.get("https://api.kanye.rest")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="Kanye West Quote",
                description=data['quote'],
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
        else:
            raise error_messages.YouMadeAMistake(value="kanye",
                                                 message=f"There was an error getting a Kanye West quote ({response.status_code})")

    @commands.command(help="Translate to Yoda")
    async def yoda(self, ctx, *, text):
        response = requests.post("https://api.funtranslations.com/translate/yoda.json", data={"text": text})
        print(response.json())
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


def setup(client):
    client.add_cog(Fun(client))
