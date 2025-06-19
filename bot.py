import discord
from discord.ext import commands
import deepl
import os
from dotenv import load_dotenv
import bot_related_functions
import asyncio
from datetime import datetime
import random
from Cogs import DailyCog

start = datetime.now()

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEEPL_KEY = os.getenv('DEEPL_KEY')

translator = deepl.Translator(DEEPL_KEY)

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

RUN_ONCE = False
async def run_once_on_startup():
    global RUN_ONCE
    if not RUN_ONCE:
        try:
            await add_cogs()
            synced = await bot.tree.sync()
            print("Commands synced: " + str(len(synced)))
        except Exception as e:
            print(e)
    RUN_ONCE = True

@bot.event
async def on_ready():
    print(str(bot.user) + " is running!")
    await run_once_on_startup()
    
@bot.event
async def on_message(msg):
    if msg.content == "!!!Sync":
        global RUN_ONCE
        RUN_ONCE = False
        run_once_on_startup()

@bot.tree.command(description="Translate a phrase to English.")
@discord.app_commands.describe(translate="need translated")
async def translate(interaction: discord.Interaction, translate: str):
    rawMessage = translate
    rawMessage.strip()
    translated_message = translator.translate_text(rawMessage, target_lang="EN-GB")
    await interaction.response.send_message(translated_message)

@bot.tree.command(description="Flip a coin. Head or Tail!")
async def flip(interaction: discord.Interaction):
    coin = random.randint(0, 1)
    side = 'Error: Nothing is being randomized'
    if coin == 0:
        side = 'Head'
    else:
        side = 'Tail'
    await interaction.response.send_message(side)

@bot.tree.command(description="Format: /rand <num1> or /rand <num1> <num2>")
async def rand(interaction: discord.Integration, first: int , second: int | None):
    if not second:
        await interaction.response.send_message(str(random.randint(1, first)))
    else:
        await interaction.response.send_message(str(random.randint(first, second)))

@bot.tree.command(description="Get every members of the server.")
async def getmembers(interaction: discord.Interaction):
    guild = interaction.guild
    members = ""
    for i in guild.members:
        members += "\n"
        members += str(i.name)
        members += ": "
        members += str(i.id)
    smessage = "There are " + str(guild.member_count) + ". They are: " + members
    await interaction.response.send_message(smessage)
    

async def add_cogs():
    await bot.add_cog(DailyCog(bot))
    print("Cog added")

    
bot.run(DISCORD_TOKEN)
