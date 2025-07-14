import discord
from discord.ext import tasks, commands
import datetime
import bot_related_functions
import os
from dotenv import load_dotenv

utc = datetime.timezone.utc
leetcode_time = datetime.time(hour=0, minute=0, tzinfo=utc)
coop_time = datetime.time(hour=13, minute=30, tzinfo=utc)

load_dotenv()
LEETCODE_CHANNEL = os.getenv('LEETCODE_CHANNEL')
GENERAL_CHANNEL = os.getenv('GENERAL_CHANNEL')

class DailyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leetcode_daily.start()
        self.coop_weekends_notice.start()
        
    def cog_unload(self):
        self.leetcode_daily.cancel()
        self.coop_weekends_notice.cancel()
    
    @tasks.loop(time=leetcode_time)
    async def leetcode_daily(self):
        channelid = int(LEETCODE_CHANNEL)
        channel = self.bot.get_channel(channelid)
        if channel:
            herf_daily = bot_related_functions.get_daily_leetcode_screenshot()
            await channel.send(herf_daily, suppress_embeds=True)
            await channel.send(file=discord.File('daily.png'))
            print(f"Channel with ID {channelid} has been sent daily challenge")
        else:
            print(f"Channel with ID {channelid} not found.")
            
    @tasks.loop(time=coop_time)
    async def coop_weekends_notice(self):
        channelid = int(GENERAL_CHANNEL)
        channel = self.bot.get_channel(channelid)
        
        if datetime.datetime.now().weekday() < 5:
            return
        
        members = bot_related_functions.members_to_notify()
        
        if not channel:
            print("Coop channel to notify doesn't exist")

        notify_message = "It's time to Co-op "
        for i in members:
            notify_message += "<@" + str(i) + "> "
        await channel.send(notify_message)
        print("Notified")
