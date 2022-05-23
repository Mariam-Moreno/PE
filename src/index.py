import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
from urllib import parse, request
import re
import youtube_dl


intents = discord.Intents.default()  
intents.members = True
bot = commands.Bot(command_prefix = '!', description = "This is an entertainment bot", help_command = None, intents = intents)


#Banco de preguntas
preguntas = ["¿Cómo estás?", "¡Qué tal?"]


#Función que registra todas las acciones
def analiticas(valor):
    f = open("C:/Users/danie/OneDrive/Documentos/LIS/LIS - Segundo Semestre/Programación Estructurada/PE/src/analiticas.txt", "a")
    f.write(valor)
    f.close()


#Analíticas
@bot.command()
async def analytics(ctx):
    musica = 0; preguntas = 0; yt = 0; hp = 0
    cont = 0
    f = open("C:/Users/danie/OneDrive/Documentos/LIS/LIS - Segundo Semestre/Programación Estructurada/PE/src/analiticas.txt","r")
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
    analiticas("H")

    des = """
    Comandos de Bot\n

    - Prefix:  !\n

    > preguntaAleatoria: El bot de pregunta algo interesante\n

    > Youtube: Encuentra un video de Youtube\n

    > conect: El bot se conectará al chat de voz donde estés\n

    > disconect: El bot se desconectará del chat de voz donde esté\n

    > play: Reproduce música por medio de un link de Youtube\n

    > pause: Pone pausa a la canción\n

    > resume: Reanuda la canción\n

    > stop: Detiene la canción\n

    Hecho con amor en Python\n
    """
    embed = discord.Embed(title="Bot del Servidor",description = des,
    timestamp = datetime.datetime.utcnow(),
    color = discord.Color.blue())
    embed.set_footer(text = "solicitado por: {}".format(ctx.author.name))
    embed.set_author(name = "Owner: {}".format(ctx.guild.owner),       
    icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Logo_UADY.svg/292px-Logo_UADY.svg.png")

    await ctx.send(embed = embed)


#Preguntas aleatorias
@bot.command()
async def pregunta(ctx):
    analiticas("P")
    await ctx.send(random.choice(preguntas))


#Buscar videos en Youtube
@bot.command()
async def youtube(ctx, *, search):
    analiticas("Y")
    query_string = parse.urlencode({'search_query': search})
    htmlContent = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('watch\?v=(.{11})',htmlContent.read().decode('utf-8'))
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


#Poner música
@bot.command()
async def conectar(ctx):
    analiticas("M")
    
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
    analiticas("M")
    voz = get(bot.voice_clients, guild = ctx.guild)
    await voz.disconnect()
    await ctx.send("Bye bye")

@bot.command()
async def play(ctx, *, search):
    analiticas("M")

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
    analiticas("M")
    await ctx.send('Pausado')
    await ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    analiticas("M")
    await ctx.send('Reanudado')
    await ctx.voice_client.resume()

@bot.command()
async def stop(ctx):
    analiticas("M")
    await ctx.send('Música detenida')
    await ctx.voice_client.stop()


#Estado del Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Faraón Love Shady"))
    print(f"My bot {bot.user} is ready")


bot.run('OTU4NjMyNjQwNTk0OTcyNjgy.G0nYEy.uaZO9dmacXT_fZnnMIS5xAjtdP6xwn5yWSFQmA')