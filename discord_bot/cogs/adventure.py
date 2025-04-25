import discord
from discord.ext import commands
import aiohttp  

class Adventure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="list_adventures", description="List all available adventures")
    async def list_adventures(self, interaction: discord.Interaction):
        """
        Command to list all available adventures.
        """
        api_url = "http://127.0.0.1:8000/adventures/list/"

        async with aiohttp.ClientSession() as session: 
            try:
                async with session.get(api_url) as response: 
                    if response.status in range(200, 300):
                        data = await response.json()
                        adventure_names = [adventure["name"] for adventure in data]
                        if adventure_names:
                            await interaction.response.send_message(f"Available adventures: {', '.join(adventure_names)}")
                        else:
                            await interaction.response.send_message("No adventures available at the moment.")
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.")
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}")
                return


async def setup(bot):
    await bot.add_cog(Adventure(bot))