import discord
from discord.ext import commands

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction, bet: int, side: str):
        """
        Flip a coin and check if you win or lose.
        """
        if side.lower() not in ["heads", "tails"]:
            await interaction.response.send_message("Please choose either 'heads' or 'tails'.")
            return

        import random
        result = random.choice(["heads", "tails"])

        if result == side.lower():
            await interaction.response.send_message(f"You won! The coin landed on {result}.")
        else:
            await interaction.response.send_message(f"You lost! The coin landed on {result}.")

async def setup(bot):
    await bot.add_cog(Gamble(bot))