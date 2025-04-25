import discord
from discord.ext import commands
import aiohttp  

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="coinflip", description="Flip a coin and place a bet")
    async def coinflip(self, interaction: discord.Interaction, bet: int, side: str):
        """
        Flip a coin, place a bet, and check if you win or lose.
        """
        if side.lower() not in ["heads", "tails"]:
            await interaction.response.send_message("Please choose either 'heads' or 'tails'.")
            return

        if bet <= 0:
            await interaction.response.send_message("Your bet must be a positive integer.")
            return

        discord_id = str(interaction.user.id)
        username = interaction.user.name

        api_url = "http://127.0.0.1:8000/users/coinflip/"  

        payload = {
            "discord_id": discord_id,
            "username": username,
            "bet": bet,
            "side": side
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                if response.status in range(200, 300):
                    data = await response.json()
                    message = data.get("message", "Something went wrong.")
                    await interaction.response.send_message(message)
                elif response.status in range (400, 500):
                    error = await response.json()
                    await interaction.response.send_message(f"Error: {error.get('error', 'Invalid request.')}")
                else:
                    await interaction.response.send_message("An unexpected error occurred. Please try again later.")

async def setup(bot):
    await bot.add_cog(Gamble(bot))