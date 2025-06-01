import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
import Gemini
from Gemini import history

# command prefix
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = commands.Bot(command_prefix="!", intents=intents)

# Load .env from the directory where THIS script lives
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")

#inits
gemini = Gemini.Gemini()

class Client(discord.Client):
    async def on_ready(self):
        start = gemini.start()
        
        # triggered on connect
        print(f'Logged in as {client.user}')
        
        # Get all the guilds
        for guild in client.guilds:
            #send to general
            channel = guild.text_channels[0]
            await channel.send(start)
            history.update_history(gemini.start_string, "bot",True)
            print(f"Sent to {guild.name} in {channel.name}")

    async def on_message(self, message):
        # ignore messages from the bot itself
        if message.author == client.user:
            history.update_history(message.content, "bot",True)
            return
        
        history.update_history(message.content, message.author.name,False)
        response = gemini.respond_to_message(message.author,message.content)
        await message.channel.send(response)
        if "passed" in response:
            gemini.current_room += 1
            await message.channel.send(gemini.describe_room())
        if gemini.current_room >= len(gemini.rooms):
            await message.channel.send("Congratulations! You have completed the escape room!")
            gemini.game_over = True

        
        

client = Client(intents=intents)
if __name__ == "__main__":
    client.run(TOKEN)
