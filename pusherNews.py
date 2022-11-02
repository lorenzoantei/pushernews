print('StalkerNews discord bot \n')

from discord.ext import tasks
import discord
import time
from dotenv import load_dotenv
import os
load_dotenv()

def get_variable(var_name: str) -> bool: # dotenv_smart_bool.py
    TRUE_=('true', '1', 't') # Add more entries if you want, like: `y`, `yes`, ...
    FALSE_=('false', '0', 'f')
    value = os.getenv(var_name, 'False').lower()  # return `False` if variable is not set. To raise an error, change `'False'` to `None`
    if value not in TRUE_ + FALSE_:
        raise ValueError(f'Invalid value `{value}` for variable `{var_name}`')
    return value in TRUE_

debug = get_variable('DEBUG')
autoclose = get_variable('AUTOCLOSE_MODE')
if debug: print('DEBUG IS ON!!1!')

if debug: print('loaded dotenv')

TOKEN = os.getenv('DISCORD_TOKEN')
CANALE_NEWS = int(os.getenv('CHANNEL_NEWS_ID'))
INTERVAL_CHECK_TIME = int(os.getenv('INTERVAL_CHECK_TIME'))

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
        channel = self.get_channel(CANALE_NEWS)  # channel ID goes here
        if debug: print('set channel ID')

        import requests, bs4
        if debug: print('loaded requests & bs4')
        from oauth2client.service_account import ServiceAccountCredentials
        import gspread
        if debug: print('loaded gspread')
        import json
        scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("sbotsbotsbotsbot_Gcreds.json", scopes) #access the json key you downloaded earlier
        if debug: print('readed json with creds')
        file = gspread.authorize(credentials) # authenticate the JSON key with gspread
        if debug: print('login succesfully')
        sheet = file.open("pusherNews")  #open sheet
        if debug: print('loaded sheet pusherNews')
        values_list = sheet.sheet1.col_values(4)
        values_title_list = sheet.sheet1.col_values(5)
        INDEX = len(values_list)
        if debug: print('sheet has '+str(INDEX)+' cols. Set INDEX = '+str(INDEX))

        PRE_LINK = 'https://accademiacarrara.it'
        LINKS_AREA =['/it/blog', '/it/rassegna-stampa', '/it/news', '/it/segreteria/comunicazioni']
        def get_title(LINK_AREA):
            if LINK_AREA == LINKS_AREA[0]:
                return "📩 Nuovo articolo in Area BLOG"
            elif LINK_AREA == LINKS_AREA[1]:
                return "📣 Nuovo articolo nella Rassegna Stampa"
            elif LINK_AREA == LINKS_AREA[2]:
                return "Nuovo articolo in area NEWS"
            elif LINK_AREA == LINKS_AREA[3]:
                return "🎉 C'è un nuovo messaggio dalla Segreteria!"
        
        def fix_vision(link_area):
            if debug: print('fix_vision()')
            if link_area == LINKS_AREA[0]:
                return soup.find_all('div', class_='grid-item')
            elif link_area == LINKS_AREA[1]:
                return soup.find_all('td', class_='views-field') #DA FIXARE
            elif link_area == LINKS_AREA[2]:
                return soup.find_all('div', class_='blog-details') # div blog-details oppure li blog-list-wrap
            elif link_area == LINKS_AREA[3]:
                return soup.find_all('li', class_='blog-list-wrap')
        
        if debug: print('\n*********\nStarting area loop...\n*********\n')
        for link_area in LINKS_AREA:

            CURRENT_LINK = PRE_LINK + link_area #FOR EACH LINK IN LINKS[]
            if debug: print('CURRENT_LINK => '+CURRENT_LINK)
            response = requests.get(CURRENT_LINK) #fa una get request ed ottiene l'html della pagina
            response.raise_for_status() #genera eccezione se risponde con errore
            if debug: print('request done')
            soup=bs4.BeautifulSoup(response.text, 'html.parser') #prende la funzione BeautifulSoup da bs4 che estrae il testo dalla response in formato html(.parser)
            if debug: print('soup is ready! Take and eat, all of you...')

            div_annunci = fix_vision(link_area)

            if debug: print('Finding out all anchor tags...')
            for div_annuncio in reversed(div_annunci): #reversed per rispettare l'ordine di pubblicazione
                
                a_annunci = div_annuncio.find_all('a')
                if debug: 
                    if a_annunci: print('anchors links loaded!')
                # if debug: print(a_annunci)

                if debug: print('Matching results...')
                for a_annuncio in a_annunci:
                    link_annuncio = str(a_annuncio.get('href'))
                    titolo_annuncio = a_annuncio.text
                    if not link_annuncio.startswith('http'):
                        link_annuncio = PRE_LINK+link_annuncio # AGGIUNGERE FULL PATH - PROBLEMI CON LINK ESTERNI
                    if debug: print('link_annuncio => \n'+link_annuncio+'\n')
                    
                    try:
                        if debug: print('Check if already present...')
                        if link_annuncio in values_list or titolo_annuncio in values_title_list:
                            print('skipped')
                        else:
                            
                            # if debug: print ('******** IL TITOLO È '+titolo_annuncio+' *********')
                            if debug: print ('\n********CREATE NEW MESSAGE:')
                            nuovo_annuncio = str(get_title(link_area))+'\n'+titolo_annuncio+'\n'+link_annuncio
                            await channel.send(nuovo_annuncio) # invia su discord
                            if debug: print(nuovo_annuncio+'\n ********\n')
                            import datetime
                            TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            sheet.sheet1.insert_row([INDEX, TIMESTAMP, link_area, link_annuncio, titolo_annuncio, nuovo_annuncio])
                            INDEX = INDEX +1 #dumb ma evita rinterrogo GSheet API
                            if debug: print('writed into sheet. Now sleep 2 secs')
                            time.sleep(2)
                            if debug: print('Awake! Restarting loop...\n')
                        # if debug: print('questo non dovrebbe stamparsi')
                    except Exception as e: print(e)
                
                # endfor loop link annunci
                if debug: print('end loop links')
            # endfor div annunci
        #end for LINKS
        print('All done ;)')
        if autoclose: quit()
        

    @checkNews.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
