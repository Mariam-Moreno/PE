import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
from urllib import parse, request
import re
import youtube_dl
import os
from dotenv import load_dotenv

intents = discord.Intents.default()  
intents.members = True
bot = commands.Bot(command_prefix = '!', description = "This is an entertainment bot", help_command = None, intents = intents)


#Función que registra todas las acciones
def registrarAnaliticas(valor):
    f = open("analiticas.txt", "a")
    f.write(valor)
    f.close()


#Analíticas
@bot.command()
async def analiticas(ctx):
    musica = 0; preguntas = 0; yt = 0; hp = 0
    cont = 0
    f = open("analiticas.txt","r")
    texto = f.read()
    j = len(texto)
    while (cont < j):
        if (texto[cont] == 'P'):
            preguntas += 1
        elif (texto[cont] == 'M'):
            musica += 1        
        elif (texto[cont] == 'Y'):
            yt += 1    
        elif (texto[cont] == 'H'):
            hp += 1 
        cont += 1
    f.close()

    embed = discord.Embed(title=f"{ctx.guild.name}", description="Cantidad de ejecuciones en cada apartado", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Musica", value = musica)
    embed.add_field(name="Preguntas", value = preguntas)
    embed.add_field(name="Youtube", value = yt)
    embed.add_field(name="Help", value = hp)
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed = embed)


#Comando ayuda
@bot.command()
async  def  help(ctx):
    registrarAnaliticas("H")

    des = """
    Comandos del Bot\n
    - Prefix:  !\n
    """

    preguntas = """

    > pregunta: El bot de pregunta algo interesante\n

    > insertar: Puedes insertar preguntas\n

    * Advertencia *
    Añadir preguntas sin tildes ni signo de apertura.
    """

    musica = """
    > conect: El bot se conectará al chat de voz donde estés\n

    > disconect: El bot se desconectará del chat de voz donde esté\n

    > play: Reproduce música por medio de un link de Youtube\n

    > pause: Pone pausa a la canción\n

    > resume: Reanuda la canción\n

    > stop: Detiene la canción\n
    """

    yt = "> youtube: Encuentra un video de Youtube\n"

    embed = discord.Embed(title="Bot del Servidor",description = des,
    timestamp = datetime.datetime.utcnow(),
    color = discord.Color.blue())
    embed.set_footer(text = "solicitado por: {}".format(ctx.author.name))
    embed.set_author(name = "Owner: {}".format(ctx.guild.owner),       
    icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Logo_UADY.svg/292px-Logo_UADY.svg.png")

    embed.add_field(name="Musica", value = musica)
    embed.add_field(name="YouTube", value = yt)
    embed.add_field(name="Preguntas Aleatorias", value = preguntas)

    await ctx.send(embed = embed)


#Preguntas aleatorias
@bot.command()
async def pregunta(ctx):
    registrarAnaliticas("P")

    archivoPreguntas = open("preguntas.txt","r")
    preguntas = archivoPreguntas.readlines()
    contPreguntas = len(preguntas)
    await ctx.send(preguntas[random.randint(0,contPreguntas)])
    archivoPreguntas.close()

@bot.command( )
async def insertar(ctx, *, arg):
    p = "\n" + arg
    f = open("preguntas.txt","a")
    f.write(p)
    f.close()
    await ctx.send(p)


#Buscar videos en Youtube
@bot.command()
async def youtube(ctx, *, search):
    registrarAnaliticas("Y")
    query_string = parse.urlencode({'search_query': search})
    htmlContent = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('watch\?v=(.{11})',htmlContent.read().decode('utf-8'))
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


#Poner música
@bot.command()
async def conectar(ctx):
    registrarAnaliticas("M")
    
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
    registrarAnaliticas("M")
    voz = get(bot.voice_clients, guild = ctx.guild)
    await voz.disconnect()
    await ctx.send("Bye bye")

@bot.command()
async def play(ctx, *, search):
    registrarAnaliticas("M")

    query_string = parse.urlencode({'search_query': search})
    htmlContent = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('watch\?v=(.{11})',htmlContent.read().decode('utf-8'))
    url = 'https://www.youtube.com/watch?v=' + search_results[0]


    ctx.voice_client.stop()

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': "bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download = False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)

    await ctx.send("Reproduciendo " + search)

@bot.command()
async def pause(ctx):
    registrarAnaliticas("M")
    await ctx.send('Pausado')
    await ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    registrarAnaliticas("M")
    await ctx.send('Reanudado')
    await ctx.voice_client.resume()

@bot.command()
async def stop(ctx):
    registrarAnaliticas("M")
    await ctx.send('Música detenida')
    await ctx.voice_client.stop()


#Estado del Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Faraón Love Shady"))
    print(f"My bot {bot.user} is ready")

load_dotenv()

bot.run(os.getenv("token"))