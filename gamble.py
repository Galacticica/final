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
import random

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

        def format_response(result):
            '''
            Helper function to format the response from the API.
            '''

            embed = discord.Embed(
                title=f"{"You Won" if result['win'] else "You Lost"}!",
                description=f"The coin landed on **{result['result']}**!",
                color=discord.Color.green() if result['win'] else discord.Color.red()
            )

            embed.add_field(
                name="Your New Balance",
                value=f"**{result['balance']}**",
                inline=False
            )
            embed.set_footer(text=f"{"Congrats" if result['win'] else "Better Luck Next Time!"}")
            return embed


        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status in range(200, 300):
                        data = await response.json()
                        embed = format_response(data)
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range (400, 500):
                        error = await response.json()
                        error = error['error']['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)
    
    @gamble_group.command(name="slots", description="Play a slot machine game")
    @discord.app_commands.describe(bet="The amount of money to bet")
    async def slots(self, interaction: discord.Interaction, bet: int):
        """
        Play a slot machine game.
        """

        if bet <= 0:
            await interaction.response.send_message("Your bet must be a positive integer.", ephemeral=True)
            return

        discord_id = str(interaction.user.id)
        
        api_url = "http://127.0.0.1:8000/users/slots/"
        payload = {
            "discord_id": discord_id,
            "bet": bet
        }

            

        async def spin_slots(interaction, emojis, data):
            '''
            Helper function to create an embed for the slot machine result.
            '''

            import asyncio

            embed = discord.Embed(
                title="🎰 Slot Machine 🎰",
                description=f"**Slots:** {emojis[5]} | {emojis[5]} | {emojis[5]}",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Good luck!")
            await interaction.response.send_message(embed=embed)

            await asyncio.sleep(2)
            embed.set_footer(text="Spinning...")
            
            message = await interaction.original_response()

            for _ in range(15):
                slot1 = random.choice(emojis)
                slot2 = random.choice(emojis)
                slot3 = random.choice(emojis)
                embed.description = f"**Slots:** {slot1} | {slot2} | {slot3}"
                await message.edit(embed=embed)
                await asyncio.sleep(1)
            
            slot1 = data['slots'][slot1]
            slot2 = data['slots'][slot2]
            slot3 = data['slots'][slot3]
            embed.description = f"**Slots:** {slot1} | {slot2} | {slot3}"

            
            embed.color = discord.Color.green() if data['win'] else discord.Color.red()
            embed.add_field(
                name="You Won!",
                value=data['message'],
                inline=False
            )
            embed.set_footer(text=f"{"Congrats!" if data['win'] else "Better Luck Next Time!"}")
            await message.edit(embed=embed)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status in range(200, 300):
                        data = await response.json()
                        emojis = data['emojis']
                        await spin_slots(interaction, emojis, data)

                    elif response.status in range(400, 500):
                        error = await response.json()
                        error = error['error']['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)



async def setup(bot):
    '''
    Load the Gamble cog.
    '''

    await bot.add_cog(Gamble(bot))