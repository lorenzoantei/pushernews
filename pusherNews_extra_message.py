print('StalkerNews discord bot \n')

import discord, time, datetime, os
from discord.ext import tasks


from dotenv import load_dotenv
load_dotenv()

def get_variable(var_name: str) -> bool: # dotenv_smart_bool.py
    TRUE_=('true', '1', 't') # Add more entries if you want, like: `y`, `yes`, ...
    FALSE_=('false', '0', 'f')
    value = os.getenv(var_name, 'False').lower()  # return `False` if variable is not set. To raise an error, change `'False'` to `None`
    if value not in TRUE_ + FALSE_:
        raise ValueError(f'Invalid value `{value}` for variable `{var_name}`')
    return value in TRUE_

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

debug = get_variable('DEBUG')
is_mobile = get_variable(os.getenv('IS_MOBILE'))
autoclose = get_variable('AUTOCLOSE_MODE')

if debug: print('DEBUG IS ON!!1!')
if is_mobile: print('MOBILE MODE')
if debug: print('loaded dotenv')

TOKEN = os.getenv('DISCORD_TOKEN')
CANALE_NEWS = int(os.getenv('CHANNEL_NEWS_ID'))
MOD_ID = int(os.getenv('MOD_ID'))
INTERVAL_CHECK_TIME = int(os.getenv('INTERVAL_CHECK_TIME'))
extra_message = str(os.getenv('EXTRA_MESSAGE'))

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        extra_message = "Ciao a tutti! \n\naccademiacarrara.it è down da questa mattina :/ \n Il bot riprenderà a funzionare appena il sito tornerà disponibile..."
        await channel_news.send(extra_message) # invia su discord

        #invia su telegram
        url = f"https://api.telegram.org/bot5458532842:AAFbqZ3KakJ8KvRrwBwNIUDk-zFbpRgbEwE/sendMessage?chat_id='-1001853721028'&text='test'"
        requests.get(url)
        if autoclose: 
            if not is_mobile: quit()
        
    @checkNews.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
