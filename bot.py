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
LEETCODE_CHANNEL = os.getenv('LEETCODE_CHANNEL')
COOP_CHANNEL = os.getenv('COOP_CHANNEL')

translator = deepl.Translator(DEEPL_KEY)

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)



##### EVENTS #####

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
        await run_once_on_startup()
        
# Add steam link to the database of coop proposal
@bot.event
async def on_message(message):
    if (bot_related_functions.is_steam_store_link(message.content)
        and message.channel.id == COOP_CHANNEL):
        print("Added a game to the database")
        bot_related_functions.add_to_coop_proposal_database(message)
        response = bot_related_functions.show_coop_proposal_entry(message.content)
        await message.channel.send(response, suppress_embeds=True)



##### COMMANDS #####

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
    
@bot.tree.command(description="Get the Leetcode challenge now!")
async def leetcode(interaction: discord.Interaction):
    channelid = int(LEETCODE_CHANNEL)
    channel = bot.get_channel(channelid)
    if channel:
        herf_daily = bot_related_functions.get_daily_leetcode_screenshot()
        await channel.send(herf_daily)
        await channel.send(file=discord.File('daily.png'))
        print(f"Channel with ID {channelid} has been sent daily challenge")
    else:
        print(f"Channel with ID {channelid} not found.")
        
@bot.tree.command(description="Fetch coop proposal. Parameters optionals.")
async def coop_proposal_fetch(interaction: discord.Interaction, provided_channel: str, year: int | None, month: int | None, day: int | None):
    if provided_channel:
        channel = bot.get_channel(int(provided_channel))
    else:
        channel = interaction.channel
    
    if not year or not month or not day:
        after_date = None
    else:
        after_date = datetime.strptime(year + "-" + month + "-" + day, "%Y-%m-%d")
        
    # Discord allow 3s to response to the command
    # Using defer extend that time and show a loading bar in the chat
    await interaction.response.defer()
    
    async for message in channel.history(limit=None, after=after_date):
        bot_related_functions.add_to_coop_proposal_database(message)
    
    # Response to the defer
    await interaction.followup.send("List compiled")
    
@bot.tree.command(description="Show a coop proposal")
async def coop_proposal_show_entry(interaction: discord.Interaction, steam_link: str):
    response = bot_related_functions.show_coop_proposal_entry(steam_link)
    await interaction.response.send_message(response, suppress_embeds=True)
    
@bot.tree.command(description="Show all coop proposal entries.")
async def coop_proposal_show_all(interaction: discord.Interaction):
    response = bot_related_functions.show_all_coop_proposal_entry()
    await interaction.response.send_message(response)

@bot.tree.command(description="Show all agreed/undecided entries.")
async def coop_proposal_show_agreed(interaction: discord.Interaction, agreed: bool):
    response = bot_related_functions.show_all_agreed_coop_proposal(agreed)
    results = response.splitlines()
    pass
    
@bot.tree.command(description="Delete a coop proposal.")
async def coop_proposal_delete_entry(interaction: discord.Interaction, steam_link:str):
    result = bot_related_functions.delete_coop_proposal_entry(steam_link)
    if not result:
        response = "No matching title or no deletion was made."
    else:
        response = "Entry deleted."
    await interaction.response.send_message(response)

@bot.tree.command(description="Change a game to agree|undecided.")
async def coop_proposal_update_state(interaction: discord.Interaction, steam_link:str):
    result = bot_related_functions.change_agreed_state_coop_proposal_entry(steam_link)
    if not result:
        response = "No matching title was found or no change was made."
    else:
        response = "Entry updated."
    await interaction.response.send_message(response)

##### COGS #####

async def add_cogs():
    await bot.add_cog(DailyCog(bot))
    print("Cog added")

    
bot.run(DISCORD_TOKEN)
