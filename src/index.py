import discord
from discord.ext import commands
from discord.utils import get
import youtube


# initialize file
intents = discord.Intents.default()  
intents.members = True
bot = commands.Bot(command_prefix = '!', description = "This is an entertainment bot", help_command = None, intents=intents)

#Estado del Bot
@bot.event
async def on_ready(): # index file
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Faraón Love Shady"))
    print(f"My bot {bot.user} is ready")

bot.run('OTU4NjMyNjQwNTk0OTcyNjgy.GFJMv1.q3bcPbhKcXF0StL8oav6eyv_rj2NKGA273n1aA')
cliente=discord.Client() # https://realpython.com/how-to-make-a-discord-bot-python/#creating-a-discord-connection
obj = youtube.Youtube(bot)
#obj.youtube()
#obj.help()
#obj.preguntaAleatoria()

#EJEMPLO: https://realpython.com/how-to-make-a-discord-bot-python/#using-bot-commands
