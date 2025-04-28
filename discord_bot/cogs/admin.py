"""
File: admin.py
Author: Reagan Zierke
Date: 2025-04-22
Description: Developer commands for the bot.
These commands are intended for development and will not be in future deployment. 
"""


from discord.ext import commands
import aiohttp
import discord

class Admin(commands.Cog):
    def __init__(self, bot, dev_guild_id=756190406642761869):
        self.dev_guild_id = dev_guild_id
        self.bot = bot

    @commands.command(name="sync", description="Sync bot commands")
    @commands.is_owner()
    async def sync(self, ctx):
        '''
        Syncs the bot commands with Discord.
        '''

        try:
            print("Syncing commands...")
            commands_to_sync = self.bot.tree.get_commands()
            command_names = [command.name for command in commands_to_sync]
            await ctx.send(f"Commands to sync: {', '.join(command_names)}")
            
            synced = await self.bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} commands.")
        except Exception as e:
            await ctx.send(f"Error syncing commands: {e}")

    @commands.command(name="clear", description="Clear all slash commands")
    @commands.is_owner()
    async def clear(self, ctx):
        '''
        Clears all slash commands from the bot.
        '''

        try:
            print("Clearing commands...")
            commands_to_clear = self.bot.tree.get_commands()
            command_names = [command.name for command in commands_to_clear]
            await ctx.send(f"Commands to clear: {', '.join(command_names)}")

            guild = discord.Object(id=self.dev_guild_id)
            self.bot.tree.clear_commands(guild=guild)
            await self.bot.tree.sync(guild=guild)
            await ctx.send("All commands cleared for the development guild.")
        except Exception as e:
            await ctx.send(f"Error clearing commands: {e}")

    
    @commands.command(name="get_or_create_user", description="Get or create a user via the API")
    async def get_or_create_user(self, ctx):
        """
        Command to interact with the API and either get or create a user.
        """

        discord_id = ctx.author.id  
        discord_username = ctx.author.name  
        api_url = "http://127.0.0.1:8000/users/" 

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json={"discord_id": discord_id, "username": discord_username}) as response:
                    if response.status in (200, 201): 
                        data = await response.json()
                        await ctx.send(
                            f"User data: Username: {data['username']}, Level: {data['level']}, XP: {data['xp']}, Money: {data['money']}"
                        )
                    else:
                        error_message = await response.text()
                        await ctx.send(f"Failed to get or create user: {error_message}")
            except aiohttp.ClientError as e:
                await ctx.send(f"An error occurred while communicating with the API: {e}")


    @commands.command(name="give_money", description="Give money to a user")
    @commands.is_owner()
    async def give_money(self, ctx, user: discord.User, amount: int):
        """
        Give money to a user.
        """

        if amount <= 0:
            await ctx.send("Amount must be a positive integer.")
            return

        discord_id = str(user.id)
        api_url = "http://127.0.0.1:8000/users/give_money/"
        payload = {
            "discord_id": discord_id,
            "amount": amount
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            message = data.get("message", "Something went wrong.")
                            await ctx.send(message)
                        except aiohttp.ContentTypeError:
                            # Handle non-JSON response
                            text = await response.text()
                            await ctx.send(f"Unexpected response from the API: {text}")
                    elif response.status == 400:
                        try:
                            error = await response.json()
                            await ctx.send(f"Error: {error.get('error', 'Invalid request.')}")
                        except aiohttp.ContentTypeError:
                            # Handle non-JSON error response
                            text = await response.text()
                            await ctx.send(f"Error: {text}")
                    else:
                        await ctx.send("An unexpected error occurred. Please try again later.")
            except aiohttp.ClientError as e:
                await ctx.send(f"An error occurred while communicating with the API: {e}")

    @commands.command(name="give_xp", description="Give XP to a user")
    @commands.is_owner()
    async def give_xp(self, ctx, user: discord.User, amount: int):
        """
        Give xp to a user.
        """

        if amount <= 0:
            await ctx.send("Amount must be a positive integer.")
            return

        discord_id = str(user.id)
        api_url = "http://127.0.0.1:8000/users/give_xp/"
        payload = {
            "discord_id": discord_id,
            "amount": amount
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            message = data.get("message", "Something went wrong.")
                            await ctx.send(message)
                        except aiohttp.ContentTypeError:
                            text = await response.text()
                            await ctx.send(f"Unexpected response from the API: {text}")
                    elif response.status == 400:
                        try:
                            error = await response.json()
                            await ctx.send(f"Error: {error.get('error', 'Invalid request.')}")
                        except aiohttp.ContentTypeError:
                            text = await response.text()
                            await ctx.send(f"Error: {text}")
                    else:
                        await ctx.send("An unexpected error occurred. Please try again later.")
            except aiohttp.ClientError as e:
                await ctx.send(f"An error occurred while communicating with the API: {e}")
    
    @commands.command(name="delete_user", description="Delete a user via the API")
    @commands.is_owner()
    async def delete_user(self, ctx):
        """
        Command to delete a user via the API.
        """

        discord_id = str(ctx.author.id)
        api_url = "http://127.0.0.1:8000/users/delete_user/"
        payload = {
            "discord_id": discord_id
        }
        await ctx.send("Deleting user...")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.delete(api_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        message = data.get("message", "User successfully deleted.")
                        await ctx.send(message)
                    elif response.status == 404:
                        error = await response.json()
                        await ctx.send(f"Error: {error.get('error', 'User not found.')}")
                    elif response.status == 400:
                        error = await response.json()
                        await ctx.send(f"Error: {error.get('error', 'Invalid request.')}")
                    else:
                        await ctx.send("An unexpected error occurred. Please try again later.")
            except aiohttp.ClientError as e:
                await ctx.send(f"An error occurred while communicating with the API: {e}")


async def setup(bot):
    '''
    Load the Admin cog.
    '''

    await bot.add_cog(Admin(bot))