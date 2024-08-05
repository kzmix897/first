from telethon import TelegramClient
from telethon.tl.functions.phone import CreateCallRequest
from telethon.tl.types import InputUser
import asyncio
from datetime import datetime, timedelta
import praytimes

# Replace with your API ID and hash
api_id = '29050819'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'

# Username to call
target_username = '@xkazumih'

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Prayer Times Configuration
pray = praytimes.PrayTimes()

# Coordinates for Depok, Indonesia
latitude = -6.402484
longitude = 106.794243

def get_adzan_times():
    times = pray.getTimes(datetime.now(), (latitude, longitude), +7)
    return times

async def call_at_adzan():
    await client.start(phone)
    
    # Get user entity
    target_user = await client.get_entity(target_username)
    
    # Get adzan times
    adzan_times = get_adzan_times()
    
    # Convert adzan time to datetime object
    adzan_time = datetime.strptime(adzan_times['Maghrib'], '%H:%M')
    
    # Calculate time difference
    now = datetime.now()
    adzan_time_today = now.replace(hour=adzan_time.hour, minute=adzan_time.minute, second=0, microsecond=0)
    
    if adzan_time_today < now:
        adzan_time_today += timedelta(days=1)
    
    # Wait until adzan time
    wait_time = (adzan_time_today - now).total_seconds()
    await asyncio.sleep(wait_time)
    
    # Make a call
    await client(CreateCallRequest(user_id=InputUser(user_id=target_user.id, access_hash=target_user.access_hash)))

with client:
    client.loop.run_until_complete(call_at_adzan())
