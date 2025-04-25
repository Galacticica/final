import discord
from discord.ext import commands
import aiohttp


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="profile", description="Shows the user's current stats")
    async def profile(self, interaction: discord.Interaction):
        """
        Command to show the user's profile.
        """
        discord_id = str(interaction.user.id)
        username = interaction.user.name  
        api_url = "http://127.0.0.1:8000/users/profile/"  

        payload = {
            "discord_id": discord_id,
            "username": username
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response: 
                    if response.status in range(200, 300):
                        data = await response.json()
                        await display_profile(interaction, data)
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.")
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}")
                return



async def display_profile(interaction, data):
        """
        Helper function to display the user's profile.
        """
        username = data.get("username", "Unknown")
        level = data.get("level", 0)
        xp = data.get("xp", 0)
        money = data.get("money", 0)

        embed = discord.Embed(
            title=f"{username}'s Profile",
            color=discord.Color.blue()
        )
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="XP", value=xp, inline=True)
        embed.add_field(name="Money", value=money, inline=True)

        await interaction.response.send_message(embed=embed)
        

async def setup(bot):
    await bot.add_cog(General(bot))


    '''
    idea: have an event that on user join, it checks if the user exists in the database, if not, create a new user with default values
    admin command to create accounts for existing users
    '''