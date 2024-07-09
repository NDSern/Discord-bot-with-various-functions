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