from urllib import parse, request
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import re
import random
import datetime

preguntas = ["¿Cómo estás?", "¡Qué tal?"]

class Youtube:
    intents = discord.Intents.default()  
    intents.members = True
    bot = commands.Bot(command_prefix = '!', help_command = None, intents=intents) #atributo 

    def __init__(self, botInput): #inicializar -> self es cosas de Python ->botInput es el objeto base, el que hace que corra la app
        self.bot=botInput
    #tarea: investigar cómo declarar atributos y usar construictores en Python
    @bot.command()
    async def youtube(ctx, *, search):
        query_string = parse.urlencode({'search_query': search})
        htmlContent = request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall('watch\?v=(.{11})',htmlContent.read().decode('utf-8'))
        await ctx.send('https://www.youtube.com/watch?v=' + search_results[0]+"\nThanks!")

    @bot.command()
    async def help(ctx): # initialize file
        des = """
        Comandos de Bot\n
        > Prefix:  !\n
        > preguntaAleatoria: El bot de pregunta algo interesante\n
        > youtube: Encuentra un video de Youtube\n
        Hecho con amor en Python\n
        """
        embed = discord.Embed(title="Bot del Servidor",description = des,
        timestamp = datetime.datetime.utcnow(),
        color = discord.Color.blue())
        embed.set_footer(text = "Solicitado por: {}".format(ctx.author.name))
        embed.set_author(name = "Owner: {}".format(ctx.guild.owner),       
        icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Logo_UADY.svg/292px-Logo_UADY.svg.png")
        await ctx.send(embed=embed)

    

    #Preguntas aleatorias
    @bot.command()
    async def preguntaAleatoria(ctx): # initialize file
        await ctx.send(random.choice(preguntas))