"""
File: gamble.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Gambling commands for the bot.
This file contains commands related to gambling, including coin flipping.
"""

import discord
from discord.ext import commands
import aiohttp  

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    gamble_group = discord.app_commands.Group(name="gamble", description="Gambling commands")


    @gamble_group.command(name="help", description="Shows the help menu")
    async def help(self, interaction: discord.Interaction):
        """
        Command to show the help menu.
        """
        
        embed = discord.Embed(
            title="Help Menu",
            description="List of available commands:",
            color=discord.Color.blue()
        )

        for command in self.gamble_group.commands:
            embed.add_field(
            name=f"/gamble {command.name}",
            value=command.description or "No description available.",
            inline=False
        )

        await interaction.response.send_message(embed=embed)



    @gamble_group.command(name="coinflip", description="Flip a coin and place a bet")
    @discord.app_commands.describe(bet="The amount of money to bet", side="Heads or Tails")
    async def coinflip(self, interaction: discord.Interaction, bet: int, side: str):
        """
        Flip a coin, place a bet, and check if you win or lose.
        """

        if side.lower() not in ["heads", "tails"]:
            await interaction.response.send_message("Please choose either 'heads' or 'tails'.", ephemeral=True)
            return

        if bet <= 0:
            await interaction.response.send_message("Your bet must be a positive integer.", ephemeral=True)
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
                    print(error)
                    error = error['error']['non_field_errors']
                    print(error)
                    await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                    return
                else:
                    await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)

async def setup(bot):
    '''
    Load the Gamble cog.
    '''

    await bot.add_cog(Gamble(bot))