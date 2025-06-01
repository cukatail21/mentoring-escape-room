import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
import Gemini
from Gemini import history

# command prefix, will maybe use in the future
intents = discord.Intents.default()
intents.message_content = True  # for reading message content
client = commands.Bot(command_prefix="!", intents=intents) #bot init

# Load .env from the directory where THIS script lives
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")

#inits
gemini = Gemini.Gemini()

class Client(discord.Client):
    async def on_ready(self):
        #get gemini start message
        start = gemini.start()
        
        # triggered on connect, here for debug
        print(f'Logged in as {client.user}')
        
        # Get all the guilds
        for guild in client.guilds:

            #send to general
            channel = guild.text_channels[0]
            await channel.send(start)
            print(f"Sent to {guild.name} in {channel.name}")

    async def on_message(self, message):
        
        # ignore messages from the bot itself
        if message.author == client.user:
            return
        
        response = gemini.respond_to_message(message.author,message.content)
        await message.channel.send(response)
        
        # passed the room
        if "passed" in response:
            gemini.current_room += 1
            await message.channel.send(gemini.describe_room())

        # check if the game is over
        if gemini.current_room >= len(gemini.rooms):
            response = gemini.end_prompt()
            await message.channel.send(response)
            gemini.game_over = True

        # reset the game if the user types !reset
        if "!reset_game" in message.content.lower():
            gemini.reset_game()
            start = gemini.start()
            await message.channel.send(start)

        
        

# Create the client with specified intents
client = Client(intents=intents)

if __name__ == "__main__":
    client.run(TOKEN)