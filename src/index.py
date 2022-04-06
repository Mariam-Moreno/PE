import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
from urllib import parse, request
import re
import youtube_dl
import os

intents = discord.Intents.default()  
intents.members = True
bot = commands.Bot(command_prefix = '!', description = "This is an entertainment bot", help_command = None, intents=intents)

preguntas = ["¿Cómo estás?", "¡Qué tal?"]

@bot.command()
async  def  help(ctx):
    des = """
    Comandos de Bot\n

    > Prefix:  !\n

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

@bot.command()
async def preguntaAleatoria(ctx):
    await ctx.send(random.choice(preguntas))

@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    htmlContent = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('watch\?v=(.{11})',htmlContent.read().decode('utf-8'))
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

@bot.command()
async def conectar(ctx):
    
    if ctx.author.voice is None:
        await ctx.send("No te encuentras en un canal de voz en este momento.")
        return

    canal = ctx.message.author.voice.channel
    voz = get(bot.voice_clients, guild = ctx.guild)

    if voz and voz.is_connected():
        await voz.move_to(canal)
    else:
        voz = await canal.connect()

@bot.command()
async def desconectar(ctx):
    voz = get(bot.voice_clients, guild = ctx.guild)
    await voz.disconnect()

@bot.command()
async def play(ctx, url):
    ctx.voice_client.stop()

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': "bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download = False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)
    
#Estado del Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Faraón Love Shady"))
    print(f"My bot {bot.user} is ready")

bot.run('OTU4NjMyNjQwNTk0OTcyNjgy.YkQKOA.hq81KoA3r9yrCmqE5_RzReK0e5g')