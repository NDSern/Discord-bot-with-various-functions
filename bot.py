import discord
import deepl
import os
from dotenv import load_dotenv
import bot_related_functions
import asyncio
from datetime import datetime

start = datetime.now()

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEEPL_KEY = os.getenv('DEEPL_KEY')

translator = deepl.Translator(DEEPL_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    while not client.is_closed():
        if bot_related_functions.new_day():
            channel_id = bot_related_functions.get_subscribed_channel_id()
            channel = client.get_channel(channel_id)

            if channel:
                bot_related_functions.get_daily_leetcode_screenshot()
                await channel.send(file=discord.File('daily.png'))
                print(f"Channel with ID {channel_id} has been sent daily challenge")
            else:
                print(f"Channel with ID {channel_id} not found.")
        
        if bot_related_functions.notify_time():
            members = bot_related_functions.members_to_notify()
            channel_id = bot_related_functions.get_notify_channel(0)
            channel = client.get_channel(channel_id)
            
            if channel:
                notify_message = "It's time to Co-op "
                for i in members:
                    notify_message += "<@" + str(i.id) + "> "
                await channel.send(notify_message)
                print("Notified")
            else:
                print("Channel to notify doesn't exist")
                
        print("The bot has been up for: ", datetime.now() - start) 
        
        await asyncio.sleep(60)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/rand'):
        return

    if message.content.startswith('/translate'):
        need_translation_message = message.content[6:]
        translated_message = translator.translate_text(need_translation_message, target_lang="EN-GB")
        await message.channel.send(translated_message.text)
        
    if message.content.startswith('/leetd'):
        bot_related_functions.get_daily_leetcode_screenshot()
        await message.channel.send(file=discord.File('daily.png'))
    
    if message.content.startswith('/leetnewd'):
        bot_related_functions.get_new_daily_leetcode_screenshot()
        await message.channel.send(file=discord.File('daily.png'))
    
    if message.content.startswith('/leetsubscribe'):
        subscribed_channel_id = message.channel.id
        bot_related_functions.leetcode_daily_subscribed(subscribed_channel_id)
        await message.channel.send("Channel subscribed")
        
    if message.content.startswith("/getmembers"):
        guild = message.channel.guild
        members = ""
        for i in guild.members:
            members += "\n"
            members += str(i.name)
            members += ": "
            members += str(i.id)
            members += "\n"
        smessage = "There are " + str(guild.member_count) + ". They are: " + members
        await message.channel.send(smessage)

client.run(DISCORD_TOKEN)
