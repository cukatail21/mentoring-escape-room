import discord
from discord.ext import commands

# Define the bot with a command prefix
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_message(message):
    
        # This event is triggered when the bot has successfully connected
        print(f'Logged in as {client.user}')
        
        # Get all the guilds (servers) the bot is in
        for guild in client.guilds:
            # You can choose a specific channel in the guild where you want to send the message
            # Here, we send it to the first text channel in the guild
            channel = guild.text_channels[0]
            await channel.send('Happy Birthday! 🎈🎉')
            print(f"Sent birthday message to {guild.name} in {channel.name}")

# Run the bot with your token
client.run('TOKEN')

