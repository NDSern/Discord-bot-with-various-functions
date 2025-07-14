import datetime
import browse_web
import re
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
import os
from dotenv import load_dotenv


load_dotenv()
MONGODB_USER = os.getenv('MONGODB_USER')
MONGODB_PASS = os.getenv('MONGODB_PASS')


def new_day():
    file_date = 0
    created = True
    today = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
    
    try:
        with open('daily date.txt', 'r') as f:
            for line in f:
                file_date = line.strip()
    except FileNotFoundError:
        created = False
        print('File dont exist')
    
    if file_date != today:
        created = False
        print('Its a new day')
            
    return not created

def get_daily_leetcode_screenshot():
    if new_day():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        herf_value = browse_web.capture_daily()
        with open("daily date.txt", 'w') as f:
            f.writelines(today)
        return herf_value
    else:
        return "No link"

def get_new_daily_leetcode_screenshot():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    browse_web.capture_daily()
    with open("daily date.txt", 'w') as f:
        f.writelines(today)

def leetcode_daily_subscribed(id: int):
    with open('channels.txt', 'w') as f:
        f.writelines(str(id))
        
def get_subscribed_channel_id():
    id = 0
    try:
        with open('channels.txt', 'r') as f:
            for line in f:
                id = int(line.strip())
    except FileNotFoundError:
        print("No such file")
    return id

def notify_time():
    now = datetime.datetime.now()
    curr_hour = now.hour
    curr_minute = now.minute
    curr_second = now.second
    
    curr_time = datetime.time(curr_hour, curr_minute)
    notify_time = datetime.time(15, 30)
    
    # monday os 0 and sunday is 6
    # notify on weekends only
    if now.weekday() < 5:
        return False
    if curr_time == notify_time:
        return True
    else:
        return False
    
def members_to_notify():
    members = []
    with open('notify.txt', 'r') as f:
        for line in f:
            members.append(line.strip())
    return members

def get_notify_channel(channel: int):
    id = 0
    try:
        with open("channels.txt", 'r') as f:
            lines = f.readlines()
            if 0 <= channel < len(lines):
                print(lines[channel])
                return int(lines[channel])
            else:
                print("Error: Channel to notify doesn't exist")
                return id
    except FileNotFoundError:
        print("No such file to notify")
    return id


def connect_to_coop_database():
    # Database here
    uri = "mongodb+srv://"+MONGODB_USER+":"+MONGODB_PASS+"@cluster0.aib2ley.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    client = MongoClient(uri)
    
    collection = client['coop_proposal']['proposal']
    return collection

def is_steam_store_link(link):
    pattern = re.compile(
        r'^https?://store\.steampowered\.com/(app|bundle|sub)/\d+/?',
        re.IGNORECASE
    )
    
    if bool(pattern.match(link)):
        return True
    
    return False

def add_to_coop_proposal_database(message):    
    if not is_steam_store_link(message.content):
        return

    # Grab info from Steam link
    message_link = message.content.split('\n', 1)[0]
    message_name = message.content.split('/')[-2]

    collection = connect_to_coop_database()
    
    # Find the entry, increment count by 1
    # else Insert
    find_link = collection.find_one_and_update(
        {"name": message_name},
        {"$inc": {"suggested": 1}},
        return_document=ReturnDocument.AFTER
    )
    
    if find_link:
        return
    
    # Insert
    single = {
        "name": message_name,
        "link": message_link,
        "author": message.author.name,
        "date": message.created_at,
        "suggested": 1,
        "agreed": False,
    }
    
    collection.insert_one(single)
    
# This is for both when entering a link
# Or when called by a function
def find_coop_proposal_entry(title):
    find_title = ""
    criteria = ""
    if is_steam_store_link(title):
        find_title = title.split('\n', 1)[0]
        criteria = "link"
    else:
        find_title = title
        criteria = "name"
    
    collection = connect_to_coop_database()
        
    results = collection.find(
        {criteria: find_title}
    )
    
    return list(results)

def show_coop_proposal_entry(game):
    results = find_coop_proposal_entry(game)
    if not results:
        return "Can't find the game!"
    
    response = ""
    for res in results:
        name = res["name"] + "\n"
        link = res["link"] + "\n"
        suggested_by = "Suggested by: " + res["author"] + "\n"
        suggested_times = "Suggested time: " + str(res["suggested"]) + "\n"
        agreed = "Agreed? " + str(res["agreed"]) + "\n"
        seperator = "--------------------------------------" + "\n"
        response += name + link + suggested_by + suggested_times + agreed + seperator
    
    return response

def show_all_coop_proposal_entry():
    collection = connect_to_coop_database()
    results = collection.find()
    response = "```\n"
    
    for res in results:
        name = res["name"] + " | "
        suggested_times = "Suggested: " + str(res["suggested"]) + " | "
        agreed = "Agreed? " + str(res["agreed"]) + "\n"
        response += name + suggested_times + agreed
    response += "```"
    
    return response

def show_all_agreed_coop_proposal(agreed):
    collection = connect_to_coop_database()
    results = collection.find(
        {"agreed": agreed}
    )
    response = "```\n"
    
    for res in results:
        name = res["name"] + " | "
        suggested_times = "Suggested: " + str(res["suggested"]) + " | "
        agreed = "Agreed? " + str(res["agreed"]) + "\n"
        response += name + suggested_times + agreed
    response += "```"
    
    return response
    

def delete_coop_proposal_entry(game):
    collection = connect_to_coop_database()
    result = collection.delete_one(
        {"link": game}
    )
    return result.deleted_count > 0

def change_agreed_state_coop_proposal_entry(game:bool):
    collection = connect_to_coop_database()
    # Reverse the value of agreed field
    result = collection.update_one(
        {"link": game},
        {"$set": {"agreed": {"$not": "$agreed"}}}
    )
    
    return result.modified_count > 0
