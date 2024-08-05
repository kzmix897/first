from telethon import TelegramClient
from telethon.tl.types import InputUser
import asyncio
from datetime import datetime, timedelta
import praytimes

# Replace with your API ID and hash
api_id = '29050819'
api_hash = 'e801321d49ec12a06f52a91ee3ff284e'
phone = '+6285692226889'

# Username to call
target_username = '@xkazummi'

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Prayer Times Configuration
pray = praytimes.PrayTimes()

# Coordinates for Depok, Indonesia
latitude = -6.402484
longitude = 106.794243

def get_adzan_times():
    now = datetime.now()
    times = pray.getTimes([now.year, now.month, now.day], (latitude, longitude), +7)
    print(f"Adzan times: {times}")  # Debug line
    return times

async def call_at_adzan(adzan_name, adzan_time):
    await client.start(phone)
    
    # Get user entity
    target_user = await client.get_entity(target_username)
    
    now = datetime.now()
    adzan_time_today = now.replace(hour=int(adzan_time.split(':')[0]), minute=int(adzan_time.split(':')[1]), second=0, microsecond=0)
    
    if adzan_time_today < now:
        adzan_time_today += timedelta(days=1)
    
    wait_time = (adzan_time_today - now).total_seconds()
    await asyncio.sleep(wait_time)
    
    # Send a message
    await client.send_message(target_user, f"Time for {adzan_name} prayer. This is an automated reminder.")

async def main():
    while True:
        adzan_times = get_adzan_times()
        tasks = []

        for adzan_name, adzan_time in adzan_times.items():
            tasks.append(call_at_adzan(adzan_name, adzan_time))
        
        await asyncio.gather(*tasks)

with client:
    client.loop.run_until_complete(main())
