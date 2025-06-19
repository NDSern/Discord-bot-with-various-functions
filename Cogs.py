import discord
from discord.ext import tasks, commands
import datetime
import bot_related_functions

utc = datetime.timezone.utc
leetcode_time = datetime.time(hour=0, minute=0, tzinfo=utc)
coop_time = datetime.time(hour=13, minute=30, tzinfo=utc)

LEETCODE_CHANNEL = 829060490079895622
GENERAL_CHANNEL = 826136343021092897

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
        channel = self.bot.get_channel(LEETCODE_CHANNEL)
        if channel:
            herf_daily = bot_related_functions.get_daily_leetcode_screenshot()
            await channel.send(herf_daily)
            await channel.send(file=discord.File('daily.png'))
            print(f"Channel with ID {LEETCODE_CHANNEL} has been sent daily challenge")
        else:
            print(f"Channel with ID {LEETCODE_CHANNEL} not found.")
            
    @tasks.loop(time=coop_time)
    async def coop_weekends_notice(self):
        if datetime.datetime.now().weekday() < 5:
            return
        
        members = bot_related_functions.members_to_notify()
        channel = self.bot.get_channel(GENERAL_CHANNEL)
        
        if channel:
            notify_message = "It's time to Co-op "
            for i in members:
                notify_message += "<@" + str(i) + "> "
            await channel.send(notify_message)
            print("Notified")
        else:
            print("Coop channel to notify doesn't exist")
        