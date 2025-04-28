"""
File: help.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Help command for the bot.
This file contains the help command for the bot, which provides information about available commands.
"""

import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Shows the help menu")
    async def help(self, interaction: discord.Interaction):
        """
        Command to show the help menu.
        """
        
        embed = discord.Embed(
            title="Help Menu",
            description="List of available commands:",
            color=discord.Color.blue()
        )

        # Add commands to the embed
        for command in self.bot.tree.get_commands():
            embed.add_field(name=f"/{command.name}", value=command.description, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    '''
    Load the Help cog.
    '''
    
    await bot.add_cog(Help(bot))

