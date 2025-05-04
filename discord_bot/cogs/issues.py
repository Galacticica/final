"""
File: issues.py
Author: Reagan Zierke
Date: 2025-05-04
Description: A development file for bot testers to report issues and have them sent to me via Discord.
"""

import discord
from discord.ext import commands

class Issues(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1368625932776243310
        self.role_id = 769387261854351370
        self.welcome_message = ("Thanks for testing my bot! To get started, do /help. If you have any issues, please report them using /report_issue.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Event listener that triggers when a user joins the server.
        Sends a private message and assigns a role to the new member.
        """
        
        try:
            await member.send(self.welcome_message)
        except Exception as e:
            print(f"An unexpected error occurred while sending a welcome message to {member.name}: {e}")

        guild = member.guild
        role = guild.get_role(self.role_id)
        if role:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                print(f"Could not assign role '{role.name}' to {member.name}.")
        else:
            print(f"Role with ID {self.role_id} not found in guild '{guild.name}'.")

    @discord.app_commands.command(name="report_issue", description="Report an issue with the bot")
    async def report_issue(self, interaction: discord.Interaction, issue: str):
        """
        Command to report an issue with the bot.
        """
        
        if not issue:
            await interaction.response.send_message("Please provide a valid issue description.", ephemeral=True)
            return
        
        channel = self.bot.get_channel(self.channel_id)
        
        if channel is None:
            await interaction.response.send_message("Error: Channel not found.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="Issue Report",
            description=issue,
            color=discord.Color.red()
        )
        
        embed.set_footer(text="", icon_url=interaction.user.avatar.url)
        embed.add_field(name="Reported By:", value=interaction.user.mention, inline=False)

        
        await channel.send(embed=embed)
        await interaction.response.send_message("Your issue has been reported. Thank you!", ephemeral=True)
        
        
async def setup(bot):
    '''
    Setup function to add the Issues cog to the bot.
    '''
    await bot.add_cog(Issues(bot))
    