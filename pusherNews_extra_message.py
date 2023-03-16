import discord, time, datetime, os
from discord.ext import tasks
import requests

from dotenv import load_dotenv
load_dotenv()

print('StalkerNews discord bot \n')

def get_variable(var_name: str) -> bool: # dotenv_smart_bool.py
    TRUE_=('true', '1', 't') # Add more entries if you want, like: `y`, `yes`, ...
    FALSE_=('false', '0', 'f')
    value = os.getenv(var_name, 'False').lower()  # return `False` if variable is not set. To raise an error, change `'False'` to `None`
    if value not in TRUE_ + FALSE_:
        raise ValueError(f'Invalid value `{value}` for variable `{var_name}`')
    return value in TRUE_

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# TELEGRAM
TOKEN_TELEGRAM_BOT = str(os.getenv('TOKEN_TELEGRAM_BOT'))
CHANNEL_CHAT_ID = str(os.getenv('CHANNEL_CHAT_ID'))

debug = get_variable('DEBUG')
is_mobile = get_variable(os.getenv('IS_MOBILE'))
autoclose = get_variable('AUTOCLOSE_MODE')

if debug: print('DEBUG IS ON!!1!')
if is_mobile: print('MOBILE MODE')
if debug: print('loaded dotenv')

TOKEN_DISCORD = os.getenv('DISCORD_TOKEN')
CANALE_NEWS = int(os.getenv('CHANNEL_NEWS_ID'))
MOD_ID = int(os.getenv('MOD_ID'))
INTERVAL_CHECK_TIME = int(os.getenv('INTERVAL_CHECK_TIME'))
extra_message = str(os.getenv('EXTRA_MESSAGE'))

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_message = str(os.getenv('EXTRA_MESSAGE'))
        # self.counter = 0 # an attribute we can access from our task

    async def setup_hook(self) -> None:
        if debug: print('init pusherNews task')
        self.checkNews.start() # start the task to run in the background

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=INTERVAL_CHECK_TIME)  # task runs every 5000 seconds
    async def checkNews(self):
        if debug: print('\n*********\nBegin new loop\n*********\n')
        channel_news = self.get_channel(CANALE_NEWS)  # channel ID goes here
        
        await channel_news.send(extra_message) # invia su discord

        #invia su telegram
        url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM_BOT}/sendMessage?chat_id={CHANNEL_CHAT_ID}&text={self.extra_message}"
        requests.get(url)
        if autoclose: 
            if not is_mobile: quit()
        
    @checkNews.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN_DISCORD)
