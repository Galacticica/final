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
    print("Setting bot presence...")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name="Painfully Existing")
    )
    print('Bot is online!')

async def load_cogs():
    print("Checking cogs directory...")
    if not os.path.exists("./cogs"):
        print("Cogs directory does not exist!")
        return

    print("Cogs directory contents:", os.listdir("./cogs"))
    for filename in os.listdir("./cogs"):
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
    async with bot:
        await load_cogs()
        await bot.start(token)

asyncio.run(main())


