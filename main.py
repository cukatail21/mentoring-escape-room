import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
import Gemini

# command prefix
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Load .env from the directory where THIS script lives
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")

#init gemini
gemini = Gemini.Gemini()

class Client(discord.Client):
    async def on_ready(self):
        
        # triggered on connect
        print(f'Logged in as {client.user}')
        
        # Get all the guilds
        for guild in client.guilds:
            #send to general
            channel = guild.text_channels[0]
            await channel.send(gemini.start())
            print(f"Sent to {guild.name} in {channel.name}")

client = Client(intents=intents)
client.run(TOKEN)

