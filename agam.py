import discord
from dotenv import load_dotenv
import os
import time

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        print(f"{message.author}: {message.content}")
        if message.content.startswith('$start'):
            await message.channel.send('Welcome! I\'m McBotface')
            time.sleep(5)
            await message.channel.send('Botty McBotface')

client = MyClient(intents=intents)
client.run(TOKEN)