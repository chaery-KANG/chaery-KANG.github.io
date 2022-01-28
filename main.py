import discord
from discord.ext import commands
import os

def main():
    prefix = '=='
    intents = discord.Intents.all()

    client = commands.Bot(command_prefix = prefix, intents = intents)
    
    for filename in os.listdir('./cogs'):
        if '.py' in filename:
            filename = filename.replace('.py', '')
            client.load_extension(f"cogs.{filename}")
            
    with open('C:\\Users\\강채리\\OneDrive\\바탕 화면\\discordbot\\token.txt', 'r') as f:
        token = f.read()

    client.run(token)

if __name__ == '__main__':
    main()