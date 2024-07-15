import datetime
import browse_web

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
        browse_web.capture_daily()
        with open("daily date.txt", 'w') as f:
            f.writelines(today)
    else:
        return

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
    notify_time = datetime.time(18, 00)
    
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