"""
File: leaderboard.py
Author: Reagan Zierke
Date: 2025-04-22
Description: Developer commands for the bot.
These commands display the leaderboard and user stats.
"""


import discord
from discord.ext import commands
import aiohttp  

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    leaderboard_group = discord.app_commands.Group(name="leaderboard", description="Leaderboard commands")

    @leaderboard_group.command(name="help", description="Shows the help menu")
    async def help(self, interaction: discord.Interaction):
        """
        Command to show the help menu.
        """
        
        embed = discord.Embed(
            title="Help Menu",
            description="List of available commands:",
            color=discord.Color.blue()
        )

        for command in self.leaderboard_group.commands:
            embed.add_field(
            name=f"/leaderboard {command.name}",
            value=command.description or "No description available.",
            inline=False
        )

        await interaction.response.send_message(embed=embed) 

    def format_leaderboard(self, users, type):
        embed = discord.Embed(
            title=f"{type.title()} Leaderboard",
            description=f"Top users by {type.title()}",
            color=discord.Color.blue()
        )
        i = 1
        for user in users:
            embed.add_field(
                name=f"{i}. {user['username']}",
                value=f"{type.title()}: {user[type]}",
                inline=False
            )
            i += 1
        return embed


        

    @leaderboard_group.command(name="level", description="Display the leaderboard for levels")
    async def level(self, interaction: discord.Interaction):
        """
        Command to display the leaderboard for levels.
        This command fetches the leaderboard data from the API and formats it into an embed.
        """
        
        api_url = "http://127.0.0.1:8000/users/leaderboard/level"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as response:
                    if response.status in range(200,300):
                        data = await response.json()
                        embed = self.format_leaderboard(data, "level")
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400,500):
                        await interaction.response.send_message("Client error occurred.", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("Server error occurred.", ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)
                return

    @leaderboard_group.command(name="money", description="Display the leaderboard for money")
    async def money(self, interaction: discord.Interaction):
        """
        Command to display the leaderboard for money.
        This command fetches the leaderboard data from the API and formats it into an embed.
        """
        
        api_url = "http://127.0.0.1:8000/users/leaderboard/money"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as response:
                    if response.status in range(200,300):
                        data = await response.json()
                        embed = self.format_leaderboard(data, "money")
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400,500):
                        await interaction.response.send_message("Client error occurred.", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("Server error occurred.", ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)
                return

async def setup(bot):
    """
    Load the Leaderboard cog.
    """
    
    await bot.add_cog(Leaderboard(bot))