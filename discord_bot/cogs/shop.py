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
    ...





def setup(bot):
    '''
    Loads the Shop cog into the bot.
    '''

    bot.add_cog(Shop(bot))