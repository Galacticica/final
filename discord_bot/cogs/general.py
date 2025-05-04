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
        
    user_group = discord.app_commands.Group(name="user", description="User commands")


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        '''
        Listener to create a new user in the database when they join the server.
        '''

        if not member.bot:
            discord_id = str(member.id)
            username = member.name
            api_url = "http://127.0.0.1:8000/users/profile/"
            payload = {
                "discord_id": discord_id,
                "username": username
            }

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(api_url, json=payload) as response:
                        if response.status in range(200, 300):
                            pass
                        elif response.status in range(400, 500):
                            error = await response.json()
                            error = error['non_field_errors']
                            print(f"Error: {error[0]}")
                        else:
                            print("An unexpected error occurred. Please try again later.")
                except aiohttp.ClientError as e:
                    print(f"Network error: {str(e)}")




    @user_group.command(name="help", description="Shows the help menu")
    async def help(self, interaction: discord.Interaction):
        """
        Command to show the help menu.
        """
        
        embed = discord.Embed(
            title="Help Menu",
            description="List of available commands:",
            color=discord.Color.blue()
        )

        for command in self.user_group.commands:
            embed.add_field(
            name=f"/user {command.name}",
            value=command.description or "No description available.",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    

    @user_group.command(name="profile", description="Shows the user's current stats")
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

        async def _get_best_gear(self, interaction):
            """
            Helper function to get the best gear for the user.
            This function sends a request to the API to retrieve the user's best gear.
            The API is expected to return a list of gear items owned by the user.
            """

            discord_id = str(interaction.user.id)
            api_url = "http://127.0.0.1:8000/gear/best_items/"
            payload = {
                "discord_id": discord_id
            }
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(api_url, json=payload) as response:
                        if response.status in range(200, 300):
                            data = await response.json()
                            return data
                        elif response.status in range(400, 500):
                            error = await response.json()
                            error = error.get('error', {}).get('non_field_errors', ["An unknown error occurred."])[0]
                            await interaction.response.send_message(f"Error: {error}", ephemeral=True)
                            return
                        else:
                            await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
                            return
                except aiohttp.ClientError as e:
                    await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)
                    return

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

            best_gear_data = await _get_best_gear(self, interaction)
            xp_percent = best_gear_data['best_gear_xp']['xp_bonus'] if best_gear_data['best_gear_xp']['xp_bonus'] is not None else 0
            money_percent = best_gear_data['best_gear_money']['money_bonus'] if best_gear_data['best_gear_money']['money_bonus'] is not None else 0
            time_percent = best_gear_data['best_gear_time']['time_bonus'] if best_gear_data['best_gear_time']['time_bonus'] is not None else 0

            if xp_percent != 0:
                xp_percent = int(xp_percent) if xp_percent % 1 == 0 else xp_percent
            if money_percent != 0:
                money_percent = int(money_percent) if money_percent % 1 == 0 else money_percent
            if time_percent != 0:
                time_percent = int(time_percent) if time_percent % 1 == 0 else time_percent
        
            
            embed.add_field(name="XP Bonus", value=f"+{xp_percent}%", inline=True)
            embed.add_field(name="Money Bonus", value=f"+{money_percent}%", inline=True)
            embed.add_field(name="Time Bonus", value=f"-{time_percent}%", inline=True)

            embed.set_footer(text="Use /user level_up to level up your user.")

            await interaction.response.send_message(embed=embed)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response: 
                    if response.status in range(200, 300):
                        data = await response.json()
                        await display_profile(interaction, data)
                    elif response.status in range(400, 500):
                        error = await response.json()
                        error = error['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)
                return
            
    @user_group.command(name="level_up", description="Level up your user")
    async def level_up(self, interaction: discord.Interaction):
        """
        Command to level up the user.
        This command simulates leveling up the user and displays the new level and XP.
        It sends a request to the API to update the user's level and XP.
        The API is expected to return the new level and XP needed for the next level.
        """

        discord_id = str(interaction.user.id)
        api_url = "http://127.0.0.1:8000/users/level_up/"

        payload = {
            "discord_id": discord_id
        }

        async def format_level_up(data):
            """
            Helper function to format the level up response.
            This function creates an embed message to display the new level and XP.
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
                        error = error['error']['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)
                return

    @user_group.command(name="view_gear", description="View your owned gear")
    async def view_gear(self, interaction: discord.Interaction):
        """
        Command to view the gear owned by the user.
        This command sends a request to the API to retrieve the user's owned gear.
        The API is expected to return a list of gear items owned by the user.
        """

        discord_id = str(interaction.user.id)
        api_url = "http://127.0.0.1:8000/gear/owned_items/"
        payload = {
            "discord_id": discord_id
        }

        def format_gear(data):
            """
            Helper function to format the gear response.
            This function creates an embed message to display the gear owned by the user.
            """

            embed = discord.Embed(
                title="Your Owned Gear",
                color=discord.Color.blue()
            )
            if not data:
                embed.description = "You don't own any gear yet."
            else:
                for item in data:
                    name = item['name']
                    description = f"{f"\nXP Bonus: +{item['xp_bonus']}%" if item['xp_bonus'] != 0 else ""} {f"\nReward Bonus: +{item['money_bonus']}%" if item['money_bonus'] != 0 else ""} {f"\nTime Bonus: -{item['time_bonus']}%" if item['time_bonus'] != 0 else ""}"
                    embed.add_field(
                        name=name,
                        value=description,
                        inline=False
                    )
            embed.set_footer(text="Use /shop item_detail <item_name> to get more info on an item.")
            return embed

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url, json=payload) as response:
                    if response.status in range(200, 300):
                        data = await response.json()
                        embed = format_gear(data)
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400, 500):
                        error = await response.json()
                        error = error['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"Network error: {str(e)}", ephemeral=True)
                return



async def setup(bot):
    '''
    Loads the General cog.
    '''

    await bot.add_cog(General(bot))