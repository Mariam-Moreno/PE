from email import message
from email.headerregistry import MessageIDHeader
from turtle import color
import discord
from discord.ext import commands
import datetime
import random
from urllib import parse, request
import re

intents = discord.Intents.default()  
intents.members = True
client = discord.Client()
bot = commands.Bot(command_prefix = '!', description = "This is an entertainment bot", help_command = None, intents=intents)

preguntas = ["¿Cómo estás?", "¡Qué tal?"]

@bot.command()
async  def  help(ctx):
    des = """
    Comandos de Bot\n

    > Prefix:  !\n

    > Hola: El bot te saluda\n

    > preguntaAleatoria: El bot de pregunta algo interesante\n

    > Youtube: Encuentra un video de Youtube\n


    Hecho con amor en Python\n
    """
    embed = discord.Embed(title="Bot del Servidor",description = des,
    timestamp = datetime.datetime.utcnow(),
    color = discord.Color.blue())
    embed.set_footer(text = "solicitado por: {}".format(ctx.author.name))
    embed.set_author(name = "Owner: {}".format(ctx.guild.owner),       
    icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Logo_UADY.svg/292px-Logo_UADY.svg.png")

    await ctx.send(embed=embed)

@client.event
async def enMensaje(message):
    if (message.author == client.user):
        return

    msg = message.content

    if msg.startswith("Hola"):
        await message.channel.send("Hola")

@bot.command()
async def preguntaAleatoria(ctx):
    await ctx.send(random.choice(preguntas))

@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    htmlContent = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('watch\?v=(.{11})',htmlContent.read().decode('utf-8'))
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

#Estado del Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Faraón Love Shady"))
    print('My bot is ready')

bot.run('OTU4NjMyNjQwNTk0OTcyNjgy.YkQKOA.Kyoum7DNuB5yyA1UBqkXkVW_IWY')