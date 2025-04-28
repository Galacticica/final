"""
File: general.py
Author: Reagan Zierke
Date: 2025-04-27
Description: General commands for the bot.
This file contains general commands for the bot, including user profile display.
"""



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

        async def display_profile(interaction, data):
            """
            Helper function to display the user's profile.
            """

            username = data.get("username", "Unknown")
            level = data.get("level", 1)
            xp = data.get("xp", 0)
            money = data.get("money", 0)

            embed = discord.Embed(
                title=f"{username}'s Profile",
                color=discord.Color.purple()
            )
            embed.add_field(name="Level", value=level, inline=True)
            embed.add_field(name="XP", value=xp, inline=True)
            embed.add_field(name="Money", value=money, inline=True)

            await interaction.response.send_message(embed=embed)

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
            
    @discord.app_commands.command(name="level_up", description="Level up your user")
    async def level_up(self, interaction: discord.Interaction):
        """
        Command to level up the user.
        """

        discord_id = str(interaction.user.id)
        api_url = "http://127.0.0.1:8000/users/level_up/"

        payload = {
            "discord_id": discord_id
        }

        async def format_level_up(data):
            """
            Helper function to format the level up response.
            """

            new_level = data.get("level", 1)
            xp_needed = data.get("xp_needed", 0)
            xp = data.get("xp", 0)

            embed = discord.Embed(
                title=f"You leveled up to level {new_level}!",
                color=discord.Color.green()
            )
            embed.add_field(name="Current XP", value=xp, inline=True)
            embed.add_field(name="XP Needed for Next Level", value=xp_needed, inline=True)

            return embed


        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status in range(200, 300):
                        data = await response.json()
                        embed = await format_level_up(data)
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400, 500):
                        error = await response.json()
                        error = error.get('error', {}).get('non_field_errors', ["An unknown error occurred."])[0]
                        await interaction.response.send_message(f"Error: {error}")
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.")
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}")
                return

async def setup(bot):
    '''
    Loads the General cog.
    '''

    await bot.add_cog(General(bot))