from dis import dis
import discord
import youtube_dl
import datetime
import random
import re
import os
from discord.ext import commands
from discord.utils import get
from urllib import parse, request


intents = discord.Intents.default()  
intents.members = True
bot = commands.Bot(command_prefix = '!', description = "This is an entertainment bot", help_command = None, intents=intents)

#Banco de preguntas
preguntas = ["¿Cómo estás?", "¡Qué tal?"]

#Comando de ayuda
@bot.command()
async  def  help(ctx):
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
async def preguntaAleatoria(ctx):
    await ctx.send(random.choice(preguntas))


#Buscar videos
@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    htmlContent = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('watch\?v=(.{11})',htmlContent.read().decode('utf-8'))
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


#Bot de música
@bot.command()
async def conectar(ctx): 
    if ctx.author.voice is None:
        await ctx.send("No te encuentras en un canal de voz en este momento.")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice__client.move_to(voice_channel)
   

@bot.command()
async def desconectar(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, url:str):
    cancionActiva = os.path.isfile("cancion.mp3")
    try:
        if cancionActiva:
            os.remove("cancion.mp3")
            print("La canción se ha removido")
    except PermissionError:
        print("Hay una canción reproduciéndose")
        await ctx.send("Error: Canción reproduciéndose")
        return

    await ctx.send("Todo listo")

    voz = get(bot.voice_clients, guild = ctx.guild)

    ydl_op = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        print("Descargar cancion")
        ydl.download([url])
    
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renombrando archivo: {file}")
            os.rename(file, "cancion.mp3")
    
    voz.play(discord.FFmpegPCAudio("cancion.mp3"), after=lambda e:print("Ha terminado"))
    voz.source = discord.PCMVolumeTransformer(voz.source)
    voz.source.volume = 0.06

    nombre = name.rsplit("-", 2)
    await ctx.send(f"Reproduciendo {nombre[0]}")

@bot.command()
async def pausa(ctx):
    voz = get(bot.voice_clients, guild = ctx.guild)

    if voz and voz.is_playing():
        voz.pause()
        await ctx.send("Música pausada")
    else:
        await ctx.send("No hay música en reproducción")

@bot.command()
async def resume(ctx):
    voz = get(bot.voice_clients, guild = ctx.guild)

    if voz and voz.is_paused():
        await ctx.send("Reproduciendode nuevamente")
    else:
        await ctx.send("No se encuentra en pausa")

@bot.command()
async def stop(ctx):
    voz = get(bot.voice_clients, guild = ctx.guild)

    if voz and voz.is_playing():
        voz.stop()
        await ctx.send("Música detenida")
    else: 
        await ctx.send("No hay música en reproducción")


#Estado del Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Faraón Love Shady"))
    print(f"My bot {bot.user} is ready")

bot.run('OTU4NjMyNjQwNTk0OTcyNjgy.YkQKOA.JI1XxXGemb7zwxupta9lWMf8oMc')