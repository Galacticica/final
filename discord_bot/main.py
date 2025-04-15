import discord
from discord.ext import commands

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

@bot.tree.command(name="test", description="A test slash command", guild=dev_guild)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("This is a slash command!")

@bot.tree.command(name="hello", description="Say hello to someone", guild=dev_guild)
async def hello(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}!")

@bot.tree.command(name="ping", description="Check bot latency", guild=dev_guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.command(name="sync", description="Syncs the bot commands")
@commands.is_owner()
async def sync(ctx):
    try:
        print("Clearing and syncing commands to guild...")
        print(bot.tree.get_commands())
        x = await bot.tree.sync(guild=dev_guild)
        print(f"Synced {len(x)} commands to guild.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.command(name="clear", description="Clear all slash commands")
@commands.is_owner()
async def clear(ctx):
    try:
        print("Clearing all commands...")
        await bot.tree.clear_commands(guild=dev_guild) 
        await bot.tree.sync(guild=dev_guild) 
        print("All commands cleared.")
    except Exception as e:
        print(f"Error clearing commands: {e}")

bot.run('NzU2MTkyMTk3OTY3MDg1NzY3.GxXtKf.eQgewvU7B5gsp5vXsn8eiFX92CaEyczT7J4ai4')