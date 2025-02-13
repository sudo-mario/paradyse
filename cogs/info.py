import discord
from discord import app_commands, Interaction, Embed, ButtonStyle
from discord.ui import View, Button
from discord.ext import commands
from dotenv import dotenv_values
import json
import aiohttp
import requests

config = dotenv_values(".env")
headers = {
    "Authorization": f"Bot {config['TOKEN']}"
}

url = 'https://discord.com/api/v10/applications/{app_id}'


response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()
user_installs = data.get("approximate_user_install_count", 0)


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Show info about the bot.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def botinfo(self, interaction: discord.Interaction):
        """Show information about the bot."""
        try:
            avatar_url = (
                self.client.user.avatar.url
                if self.client.user.avatar
                else "https://cdn.discordapp.com/embed/avatars/0.png"
            )
            total_members = sum(guild.member_count for guild in self.client.guilds)
            guild_count = len(self.client.guilds)

            embed = discord.Embed(
                color=0x2b2d31,
                title=f"botinfo",
            )

            embed.set_thumbnail(url=f'{self.client.user.avatar.url}')
            embed.set_footer(icon_url=self.client.user.avatar.url)

            # embed.add_field(
            #     name="Statistics",
            #     value=(
            #         f"**Servers:** {guild_count}\n"
            #         f"**Members:** {total_members}\n"
            #         f"**Latency:** {round(self.client.latency * 100)}ms\n"
            #         f"**Installs:** {user_installs}"
            #     ),
            #     inline=False,
            # )
            embed.add_field(name="Installs",
                            value=f"``{user_installs}``",
                            inline=True)
            embed.add_field(name="Servers",
                            value=f"``{guild_count}``",
                            inline=True)
            embed.add_field(name="Ping",
                            value=f"``{round(self.client.latency * 100)}ms``",
                            inline=True)


            button = Button(style=discord.ButtonStyle.link, label="press 2 add", url=f"https://discord.com/oauth2/authorize?client_id={client_id}")

            view = View()
            view.add_item(button)

            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred: {e}", ephemeral=True
            )
            print(f"Error in botinfo command: {e}")


    @app_commands.command(description="Show bot website.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def website(self, interaction: discord.Interaction):
        embed = discord.Embed(description="**Bot's website:** ***[click](https://paradyse.bot)***")
        embed.set_footer(icon_url=self.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=False)


    @app_commands.command(name="credits", description="Show bot's credits.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def credits(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=f"<:paradyse:1324828511134814208> paradyse bot credits.",
            color=0x2b2d31
        )
        embed.add_field(
            name="dev",
            value="[ket/EdgE](https://discord.com/users/1338131792410054656)",
            inline=True
        )
        embed.add_field(
            name="own",
            value="-",
            inline=True
        )
        embed.add_field(
            name="★ mention",
            value="[cosmin](https://csyn.me/)\n[heist.lol](https://heist.lol/)",
            inline=True
        )
        embed.add_field(
            name=f"bot",
            value=f"-# ``{self.client.user.name}`` it's a bot made for fun, nothing serious.")
        embed.set_footer(text="paradyse", icon_url=self.client.user.display_avatar)
        embed.set_thumbnail(url=self.client.user.display_avatar)
        
        # Create buttons for support and invite
        invite_button = Button(label="press 2 add", url=f"https://discord.com/oauth2/authorize?client_id={self.client.user.id}")
        cosmin_button = Button(label="csyn", url="https://csyn.me")
        heist_button = Button(emoji='<:heist:1324450138898305115>',label="heist", url=f"https://heist.lol")
        
        # Add buttons to the view
        view = View()
        view.add_item(invite_button)
        view.add_item(cosmin_button)
        view.add_item(heist_button)
        
        # Send message with embed and buttons
        await interaction.response.send_message(embed=embed, view=view)   

async def setup(bot):
    await bot.add_cog(Info(bot))
