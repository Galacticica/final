import aiohttp
from discord.ext import commands


class DevTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test", description="Test command")
    @commands.is_owner()
    async def test(self, ctx):
        """
        Test command to check if the bot is working.
        """
        await ctx.send("Test command executed successfully!")

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



async def setup(bot):
    await bot.add_cog(DevTest(bot))