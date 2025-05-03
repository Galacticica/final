"""
File: shop.py
Author: Reagan Zierke
Date: 2025-05-03
Description: Shop commands for the bot.
This file contains commands related to the shop, such as buying and listing items.
This functionality is not yet implemented.
"""



import discord
from discord.ext import commands
import aiohttp  

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    shop_group = discord.app_commands.Group(name="shop", description="Shop commands")

    def format_time(self, seconds):
        '''
        Helper function to format time in seconds to a readable format.
        '''
            
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s" 
    
    @shop_group.command(name="help", description="Shows the help menu")
    async def help(self, interaction: discord.Interaction):
        """
        Command to show the help menu.
        """
        
        embed = discord.Embed(
            title="Help Menu",
            description="List of available commands:",
            color=discord.Color.blue()
        )

        for command in self.shop_group.commands:
            embed.add_field(
                name=f"/shop {command.name}",
                value=command.description or "No description available.",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @shop_group.command(name="list", description="List all items in the shop available for purchase")
    async def list_items(self, interaction: discord.Interaction):
        """
        Command to list all items in the shop.
        """

        api_url = "http://127.0.0.1:8000/gear/shop/"

        def format_embed(data):
            embed = discord.Embed(
                title="Shop Items",
                description="List of items available for purchase:",
                color=discord.Color.orange()
            )

            for item in data: 
                embed.add_field(
                    name=item['name'],
                    value=f"Cost: {item['cost']} {f"\nXP Bonus: +{item['xp_bonus']}%" if item['xp_bonus'] != 0 else ""} {f"\nReward Bonus: +{item['money_bonus']}%" if item['money_bonus'] != 0 else ""} {f"\nTime Bonus: -{item['time_bonus']}%" if item['time_bonus'] != 0 else ""}",
                    inline=False
                )

            embed.set_footer(text="Use /shop item_detail <item_name> to get more info on an item.")
            return embed

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as response:
                    if response.status in range(200,300):
                        data = await response.json()
                        if data and isinstance(data, list) and len(data) > 0:
                            embed = format_embed(data)
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message("No items for sale at the moment.")
                    elif response.status in range(400,500):
                        await interaction.response.send_message("Client error occurred.") 
                    else:
                        await interaction.response.send_message("Server error occurred.")
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred: {e}")
        
    @shop_group.command(name="item_detail", description="Get details about a specific item")
    @discord.app_commands.describe(item_name="Name of the item")
    async def item_detail(self, interaction: discord.Interaction, item_name: str):
        """
        Command to get details about a specific item.
        """

        api_url = "http://127.0.0.1:8000/gear/gear_detail/"

        payload = {
            "gear_name": item_name
        }

        def format_embed(data):
            embed = discord.Embed(
                title=data['name'],
                description=data['description'],
                color=discord.Color.green()
            )

            embed.add_field(
                name="Cost",
                value=f"{data['cost']}",
                inline=True
            )
            if data['xp_bonus'] != 0:
                embed.add_field(
                    name="XP Bonus",
                    value=f"+{data['xp_bonus']}%",
                    inline=True
                )
            if data['money_bonus'] != 0:
                embed.add_field(
                    name="Money Bonus",
                    value=f"+{data['money_bonus']}%",
                    inline=True
                )
            if data['time_bonus'] != 0:
                embed.add_field(
                    name="Time Bonus",
                    value=f"-{data['time_bonus']}%",
                    inline=True
                )

            embed.set_footer(text="Use /shop purchase <item_name> to purchase this item.")
            return embed

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url, json=payload) as response:
                    if response.status in range(200,300):
                        data = await response.json()
                        embed = format_embed(data)
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400,500):
                        await interaction.response.send_message("Client error occurred.")
                    else:
                        await interaction.response.send_message("Server error occurred.")
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred: {e}")
                




async def setup(bot):
    '''
    Loads the Shop cog into the bot.
    '''

    await bot.add_cog(Shop(bot))