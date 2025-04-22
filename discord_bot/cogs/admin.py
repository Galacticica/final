"""
File: admin.py
Author: Reagan Zierke
Date: 2025-04-22
Description: Developer commands for the bot.
"""


from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot, dev_guild_id=756190406642761869):
        '''
        Initializes the Admin cog.
        '''
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
            await self.bot.tree.clear_commands()
            await self.bot.tree.sync()
            await ctx.send("All commands cleared.")
        except Exception as e:
            await ctx.send(f"Error clearing commands: {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))