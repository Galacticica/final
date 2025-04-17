import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Responds with Pong!"""
        await interaction.response.send_message("Pong!")

    @discord.app_commands.command(name="hello", description="Say hello to someone")
    async def hello(self, interaction: discord.Interaction, name: str):
        """Responds with a greeting."""
        await interaction.response.send_message(f"Hello {name}!")

async def setup(bot):
    await bot.add_cog(General(bot))