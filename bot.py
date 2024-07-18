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
                    notify_message += "<@" + str(i) + "> "
                await channel.send(notify_message)
                print("Notified")
            else:
                print("Channel to notify doesn't exist")
                
        print("The bot is running, the time is: ", datetime.now()) 
        
        await asyncio.sleep(60)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('/clap_help'):
        list_of_commands = "**/translate <msg>**: Translate message\n"
        list_of_commands += "**/leetd**: Give a Leetcode daily problem screenshot\n"
        list_of_commands += "**/leetnewd**: Get a new Leetcode daily screenshot, in case /leetd did not update for the new daily challenge\n"
        list_of_commands += "**/leetsubscribe**: Subscribe channel to be notified everytime there is a new Leetcode daily\n"
        await message.channel.send(list_of_commands)

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
        
    if message.content.startswith("/notifynow"):
        members = bot_related_functions.members_to_notify()
        channel_id = bot_related_functions.get_notify_channel(0)
        channel = client.get_channel(channel_id)
        
        if channel:
            notify_message = "It's time to Co-op "
            for i in members:
                notify_message += "<@" + str(i) + "> "
            await channel.send(notify_message)
            print("Notified")
        else:
            print("Channel to notify doesn't exist")
            
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
        
    #Game Jam stuffs
    if message.content.startswith("/gamejam"):
        gamejaminfo = "[Pirate Software Game Jam](<https://itch.io/jam/pirate>)\n"
        gamejaminfo += "Theme to follow: Shadow & Alchemy\n"
        gamejaminfo += "[Repo](<https://github.com/NDSern/Game-Jam-7-2024>)\n"
        gamejaminfo += "[Docs](<https://drive.google.com/drive/folders/133YJRN0rvEuacpPovOMlSTYIQs4L3oKY?usp=sharing>)\n"
        gamejaminfo += "Current project: Plague Doctor from DD have a shadow cloak and go melee people\n"
        gamejaminfo += "Engine: Godot\n"
        gamejaminfo += "Art & Sound software: Haven't decided yet\n"
        await message.edit(suppress=True)
        await message.channel.send(gamejaminfo)
    
    if message.content.startswith("/jam_help"):
        commands = "**/todos**: Show the list of things to do\n"
        commands += "**/past**: Show the list of things that have been done\n"
        commands += "**/addtd <str>**: Add a new task\n"
        commands += "**/do <int>**: Mark yourself as doing something\n"
        commands += "**/done <int>**: Mark yourself as completed a task\n"
        await message.channel.send(commands)
    
    if message.content.startswith("/todos"):
        todo_list = ""
        try:
            with open('todos.txt', 'r') as f:
                for i, line  in enumerate(f):
                    todo_list += str(i) + ". " + line
        except FileNotFoundError:
            print("No such file")
        if not todo_list:
            todo_list = "Everything is done, for now."
        await message.channel.send(todo_list)
    
    if message.content.startswith("/past"):
        past_list = ""
        try:
            with open('done.txt', 'r') as f:
                for i, line  in enumerate(f):
                    past_list += str(i) + ". " + line
        except FileNotFoundError:
            print("No such file")
        if not past_list:
            past_list = "Nothing is completed"
        await message.channel.send(past_list)
    
    if message.content.startswith("/addtd"):
        todo = message.content[6:]
        with open("todos.txt", "a") as f:
            f.writelines("\n" + todo)
        await message.channel.send("Todo added.")
    
    if message.content.startswith("/do"):
        do = int(message.content[3:])
        print(do)
        lines = ""
        try:
            with open('todos.txt', 'r+') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("No such file")
            
        if do < 0 or do > len(lines):
            await message.channel.send("Task not in the list!")
            
        lines[do-1] = lines[do-1].strip() + " *Doing: " + message.author.name + "*"
        
        with open('todos.txt', 'r+') as f:
            f.writelines(lines)
        send_message = "Added *" + message.author.name + "* to task " + str(do)
        await message.channel.send(send_message)
        
    if message.content.startswith("/complete"):
        do = int(message.content[9:])
        try:
            with open('todos.txt', 'r+') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("No such file")
            
        if do < 0 or do > len(lines):
            await message.channel.send("Task not in the list!")
            
        done = lines[do-1].strip() + " *Completed: " + message.author.name + "*\n"
        to_delete = lines[do-1].strip()
        
        with open('done.txt', 'a') as f:
            f.writelines(done)
        with open('todos.txt', 'w') as f:
            for line in lines:
                if line.strip("\n") != to_delete:
                    print(line)
                    f.write(line)
            
        send_message = "*" + message.author.name + "* did task " + str(do)
        await message.channel.send(send_message)

client.run(DISCORD_TOKEN)
