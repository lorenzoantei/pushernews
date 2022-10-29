from discord.ext import tasks
import discord

from dotenv import load_dotenv
load_dotenv()
import os
TOKEN = os.getenv('DISCORD_TOKEN')
CANALE_NEWS = int(os.getenv('CHANNEL_NEWS_ID'))

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0 # an attribute we can access from our task

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.checkNews.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def checkNews(self):
        channel = self.get_channel(CANALE_NEWS)  # channel ID goes here
        
        ### ABACSCRAPE

        if new_link_annunci:
            await channel.send('nuovi!!')
        else:
            await channel.send('NESSUN NUOVO ANNUNCIO!!')
            
        self.counter += 1
        

    @checkNews.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)