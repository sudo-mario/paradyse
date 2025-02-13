import sqlite3
import discord
from discord.ext import commands
from dotenv import dotenv_values

# Load the bot token from the .env file
config = dotenv_values(".env")
TOKEN = config["TOKEN"]
ACTIVITY = "developing.."
# Initialize the bot
class MyClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for cog in ["cogs.info"]:
            await self.load_extension(cog)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.tree.sync()
        await client.change_presence(activity=discord.CustomActivity(name=f"{ACTIVITY}"))  # Call the status update method on bot startup


client = MyClient()
client.run(TOKEN)
