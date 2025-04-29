import discord
from discord.ext import commands
import aiohttp  

class Adventure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    adventure_group = discord.app_commands.Group(name="adventure", description="Adventure commands")

    def format_time(self, seconds):
        '''
        Helper function to format time in seconds to a readable format.
        '''
            
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s" 


    @adventure_group.command(name="help", description="Shows the help menu")
    async def help(self, interaction: discord.Interaction):
        """
        Command to show the help menu.
        """
        
        embed = discord.Embed(
            title="Help Menu",
            description="List of available commands:",
            color=discord.Color.blue()
        )

        for command in self.adventure_group.commands:
            embed.add_field(
            name=f"/adventure {command.name}",
            value=command.description or "No description available.",
            inline=False
        )

        await interaction.response.send_message(embed=embed) 

    @adventure_group.command(name="list", description="List all available adventures")
    async def list_adventures(self, interaction: discord.Interaction):
        """
        Command to list all available adventures.
        This command fetches the list of adventures from the API and displays them to the user.
        """

        api_url = "http://127.0.0.1:8000/adventures/list/"

        def format_adventure_list(adventures):
            '''
            Helper function to format the adventure list response.
            This function creates a Discord embed with the list of adventures.
            '''

            adventures.sort(key=lambda x: x.get("required_level", 0))

            embed = discord.Embed(
                title="Available Adventures",
                color=discord.Color.blue()
            )
            for adventure in adventures:
                adventure_name = adventure.get("name", "Unknown Adventure")
                adventure_level = adventure.get("required_level", "Unknown Level")
                adventure_time = self.format_time(adventure.get("time_to_complete", 0))
                embed.add_field(name=f"Level {adventure_level}: {adventure_name}", value=f"Time To Complete: {adventure_time}", inline=False)
                embed.set_footer(text="Use /adventure info <adventure_name> to get more info on an adventure!")
            return embed
            

        async with aiohttp.ClientSession() as session: 
            try:
                async with session.get(api_url) as response: 
                    if response.status in range(200, 300):
                        data = await response.json()
                        if data and isinstance(data, list) and len(data) > 0:
                            embed = format_adventure_list(data)
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message("No adventures available at the moment.")
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}", ephemeral=True)
                return
            
    @adventure_group.command(name="info", description="Get information about a specific adventure")
    @discord.app_commands.describe(adventure_name="The name of the adventure")
    async def adventure_info(self, interaction: discord.Interaction, adventure_name: str):
        """
        Command to get information about a specific adventure.
        This command fetches the adventure details from the API and displays them to the user.
        """

        api_url = "http://127.0.0.1:8000/adventures/detail/"
        payload = {
            "adventure_name": adventure_name
        }
        
        def format_adventure_info(adventure):
            '''
            Helper function to format the adventure info response.
            This function creates a Discord embed with the adventure details.
            '''

            adventure_name = adventure.get("name", "Unknown Adventure")
            adventure_description = adventure.get("description", "No description available.")
            required_level = adventure.get("required_level", "Unknown Level")
            time_to_complete = self.format_time(adventure.get("time_to_complete", 0))
            reward_min = adventure.get("reward_min", 0)
            reward_max = adventure.get("reward_max", 0)
            xp_min = adventure.get("xp_min", 0)
            xp_max = adventure.get("xp_max", 0)

            embed = discord.Embed(
                title=adventure_name,
                description=adventure_description,
                color=discord.Color.blue()
            )
            embed.add_field(name="Required Level", value=required_level, inline=True)
            embed.add_field(name="Time to Complete", value=time_to_complete, inline=True)
            embed.add_field(name="Reward Range", value=f"{reward_min} - {reward_max}", inline=True)
            embed.add_field(name="XP Range", value=f"{xp_min} - {xp_max}", inline=True)
            embed.set_footer(text="Use /adventure start <adventure_name> to start this adventure!")

            return embed
            

        async with aiohttp.ClientSession() as session:
            print("Connecting to API...")
            try:
                async with session.get(api_url, json=payload) as response:
                    print(f"Response status: {response.status}")
                    if response.status in range(200, 300):
                        data = await response.json()
                        embed = format_adventure_info(data)
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
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}", ephemeral=True)
                return


    @adventure_group.command(name="start", description="Start an adventure")
    @discord.app_commands.describe(adventure_name="The name of the adventure to start")
    async def start_adventure(self, interaction: discord.Interaction, adventure_name: str):
        """
        Command to start an adventure.
        This command sends a request to the API to start an adventure for the user.
        The user must provide the name of the adventure they want to start.
        """

        api_url = "http://127.0.0.1:8000/adventures/start/"

        payload = {
            "discord_id": str(interaction.user.id),
            "adventure_name": adventure_name
        }

        

        def format_start_adventure(adventure):
            '''
            Helper function to format the adventure start response.
            '''

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
                        await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}", ephemeral=True)
                return

    async def complete_adventure(self, interaction: discord.Interaction):
        """
        Function to complete an adventure.
        This function sends a request to the API to complete the adventure for the user.
        It is called when the user checks their adventure status and it is complete.
        """

        api_url = "http://127.0.0.1:8000/adventures/complete/"
        payload = {
            "discord_id": str(interaction.user.id)
        }

        def format_complete_adventure(adventure):
            '''
            Helper function to format the adventure completion response.
            '''

            adventure_name = adventure.get("adventure_name", "Unknown Adventure")
            rewarded_xp = adventure.get("xp_reward", 0)
            rewarded_money = adventure.get("money_reward", 0)

            embed = discord.Embed(
                title=f"{adventure_name} Completed!",
                color=discord.Color.green()
            )
            embed.add_field(name="XP Gained", value=rewarded_xp, inline=True)
            embed.add_field(name="Money Gained", value=rewarded_money, inline=True)
            embed.set_footer(text="Congratulations on completing your adventure!")

            return embed


        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status in range(200, 300):
                        data = await response.json()
                        embed = format_complete_adventure(data)
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
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}", ephemeral=True)
                return
            
        
    @adventure_group.command(name="status", description="Check the status of your adventure")
    async def adventure_status(self, interaction: discord.Interaction):
        """
        Command to check the status of an adventure.
        This command sends a request to the API to check the status of the user's adventure.
        If the adventure is complete, it calls the complete_adventure function.
        If the adventure is still in progress, it formats the response and sends it to the user.
        """

        api_url = "http://127.0.0.1:8000/adventures/status/"
        payload = {
            "discord_id": str(interaction.user.id)
        }

        def format_adventure_status(adventure):
            '''
            Helper function to format the adventure status response.
            This function creates a Discord embed with the adventure status information.
            '''

            adventure_name = adventure.get("name", "Unknown Adventure")
            time_left = self.format_time(adventure.get("time_left", 0))

            embed = discord.Embed(
                title=f"{adventure_name} Status",
                color=discord.Color.yellow()
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
                            await self.complete_adventure(interaction)
                            return
                        else:
                            embed = format_adventure_status(data)
                            await interaction.response.send_message(embed=embed)
                            return
                    elif response.status in range(400, 500):
                        error = await response.json()
                        error = error['non_field_errors']
                        await interaction.response.send_message(f"Error: {error[0]}", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                await interaction.response.send_message(f"An error occurred while communicating with the API: {e}", ephemeral=True)
                return



async def setup(bot):
    '''
    Load the Adventure cog.
    '''

    await bot.add_cog(Adventure(bot))