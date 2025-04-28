"""
File: main.py
Author: Reagan Zierke
Date: 2025-04-22
Description: Main file for the Discord bot.
This file initializes the bot, loads cogs, and starts the bot.
"""


import pathlib
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
dev_guild = discord.Object(id=756190406642761869)

@bot.event
async def on_ready():
    '''
    Event triggered when the bot is ready.
    '''

    print("Setting bot presence...")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name="Painfully Existing")
    )
    print('Bot is online!')

async def load_cogs():
    '''
    Loads all cogs from the cogs directory.
    '''

    print("Checking cogs directory...")
    print(pathlib.Path.cwd())
    if not os.path.exists("discord_bot/cogs"):
        print("Cogs directory does not exist!")
        return

    print("Cogs directory contents:", os.listdir("discord_bot/cogs"))
    for filename in os.listdir("discord_bot/cogs"):
        if filename.endswith(".py"):
            try:
                print(f"Loading cog: {filename}")
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("Discord token not found in .env file!")

async def main():
    '''
    Runs the main function to start the bot.
    '''

    async with bot:
        await load_cogs()
        await bot.start(token)

asyncio.run(main())


