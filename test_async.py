import discord, time, datetime, os
from discord.ext import tasks


@tasks.loop(seconds=5)  # decoratore per indicare che verrà eseguita ogni INTERVAL_CHECK_TIME seconds
async def checkNews(self): # definizione della chiamata asincrona ripetuta come indicato sopra
    print("5 secondi passati")
