import discord
from discord.ext import commands
import aiohttp  

class Adventure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_time(self, seconds):
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"  

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
            
    @discord.app_commands.command(name="start_adventure", description="Start an adventure")
    async def start_adventure(self, interaction: discord.Interaction, adventure_name: str):
        """
        Command to start an adventure.
        """
        api_url = "http://127.0.0.1:8000/adventures/start/"

        payload = {
            "discord_id": str(interaction.user.id),
            "adventure_name": adventure_name
        }

        

        def format_start_adventure(adventure):
            adventure_name = adventure.get("name", "Unknown Adventure")
            time_left = self.format_time(adventure.get("time_left", 0))

            embed = discord.Embed(
                title=f"{adventure_name} Started!",
                color=discord.Color.blue()
            )
            embed.add_field(name="Time Left", value=time_left, inline=True)
            embed.set_footer(text="Good luck on your adventure!")

            return embed


        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status in range(200, 300):
                        data = await response.json()
                        embed = format_start_adventure(data)
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400, 500):
                        error = await response.json()
                        error = error['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}")
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.")
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}")
                return

        
        
    @discord.app_commands.command(name="adventure_status", description="Check the status of your adventure")
    async def adventure_status(self, interaction: discord.Interaction):
        """
        Command to check the status of an adventure.
        """
        api_url = "http://127.0.0.1:8000/adventures/status/"
        payload = {
            "discord_id": str(interaction.user.id)
        }

        def format_adventure_status(adventure):
            adventure_name = adventure.get("name", "Unknown Adventure")
            time_left = self.format_time(adventure.get("time_left", 0))

            embed = discord.Embed(
                title=f"{adventure_name} Status",
                color=discord.Color.green()
            )
            embed.add_field(name="Time Left", value=time_left, inline=True)
            embed.set_footer(text="Stay strong on your adventure!")

            return embed        
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status in range(200, 300):
                        data = await response.json()
                        if data.get("complete"):
                            await interaction.response.send_message("Your adventure is complete! You can now claim your rewards.")
                        else:
                            embed = format_adventure_status(data)
                            await interaction.response.send_message(embed=embed)
                    elif response.status in range(400, 500):
                        error = await response.json()
                        error = error['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}")
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.")
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}")
                return

    






            
        

      

async def setup(bot):
    await bot.add_cog(Adventure(bot))