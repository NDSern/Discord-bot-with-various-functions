import discord
from discord.ext import commands

class PaginationView(discord.ui.View):
    current_page = 1
    
    async def send(interaction: discord.Interaction):
        await interaction.response.send_message()