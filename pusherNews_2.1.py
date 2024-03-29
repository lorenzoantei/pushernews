import discord, time, datetime, os
from discord.ext import tasks
from dotenv import load_dotenv
import requests, bs4
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json

import random
import datetime
from pytz import timezone

start_time = datetime.time(hour=9, minute=0)
end_time = datetime.time(hour=19, minute=0)
time_zone = timezone('Europe/Rome')

PRE_LINK = 'https://accademiacarrara.it'
LINKS_AREA =['/it/blog', '/it/rassegna-stampa', '/it/news', '/it/segreteria/comunicazioni']

def get_title(LINK_AREA):
    if LINK_AREA == LINKS_AREA[0]:
        return "🎉 Nuovo articolo in Area BLOG"
    elif LINK_AREA == LINKS_AREA[1]:
        return "📣 Nuovo articolo nella Rassegna Stampa"
    elif LINK_AREA == LINKS_AREA[2]:
        return "Nuovo articolo in area NEWS"
    elif LINK_AREA == LINKS_AREA[3]:
        return "📩 C'è un nuovo messaggio dalla Segreteria!"

def fix_vision(soup, link_area):
    if debug: print('right soup into CURRENT AREA...')
    if link_area == LINKS_AREA[0]:
        return soup.find_all('div', class_='grid-item')
    elif link_area == LINKS_AREA[1]:
        return soup.find_all('td', class_='views-field') #DA FIXARE
    elif link_area == LINKS_AREA[2]:
        return soup.find_all('div', class_='blog-details') # div blog-details oppure li blog-list-wrap
    elif link_area == LINKS_AREA[3]:
        return soup.find_all('li', class_='blog-list-wrap')

def get_variable(var_name: str) -> bool: 
    TRUE_=('true', '1', 't') # Add more entries if you want, like: `y`, `yes`, ...
    FALSE_=('false', '0', 'f')
    value = os.getenv(var_name, 'False').lower()  # return `False` if variable is not set. To raise an error, change `'False'` to `None`
    if value not in TRUE_ + FALSE_:
        raise ValueError(f'Invalid value `{value}` for variable `{var_name}`')
    return value in TRUE_

print('StalkerNews discord bot \n')

load_dotenv()

debug = get_variable('DEBUG')
if debug: print('DEBUG IS ON!!1!')
if debug: print('loaded dotenv')

TESTINGMODE = get_variable('TESTINGMODE')
if debug: 
    if TESTINGMODE: print('TESTINGMODE')

# GOOGLE SHEET
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name("sbotsbotsbotsbot_Gcreds.json", scopes) #access the json key you downloaded earlier
if debug: print('readed json with creds')

file = gspread.authorize(credentials) # authenticate the JSON key with gspread
if debug: print('login succesfully')

# TELEGRAM
TOKEN_TELEGRAM_BOT = str(os.getenv('TOKEN_TELEGRAM_BOT'))
CHANNEL_CHAT_ID = str(os.getenv('CHANNEL_CHAT_ID'))

# DISCORD
TOKEN = os.getenv('DISCORD_TOKEN')
CANALE_NEWS = int(os.getenv('CHANNEL_NEWS_ID'))
MOD_ID = int(os.getenv('MOD_ID'))
MIN_VAL_CHECK_TIME = int(os.getenv('MIN_VAL_CHECK_TIME'))
MAX_VAL_CHECK_TIME = int(os.getenv('MAX_VAL_CHECK_TIME'))


class MyClient(discord.Client): # Definizione della classe MyClient che eredita da discord.Client
    def __init__(self, *args, **kwargs): # Costruttore della classe, viene chiamato quando si istanzia un oggetto di tipo MyClient
        super().__init__(*args, **kwargs) # Chiamata al costruttore della classe genitore (discord.Client)

        # variabili usate dalla chiamata async
        self.sheet = file.open("pusherNews")  #open sheet
        self.values_list = self.sheet.sheet1.col_values(4)

       

        self.values_title_list = self.sheet.sheet1.col_values(5)
        self.INDEX = len(self.values_list)


        # Apri il foglio di lavoro
        # client = gspread.authorize(creds)
        sheet = file.open('pusherNews').worksheet('CORRENTI')
        # print(sheet)
        



        # quit()

        # self.tab_archive = self.sheet.worksheet('ARCHIVE')
        # self.tab_correnti = self.sheet.worksheet('CORRENTI')
        self.tab_correnti = file.open('pusherNews').worksheet('CORRENTI')
        self.tab_archive = file.open('pusherNews').worksheet('ARCHIVE')

        self.array_cleanup = [] # init array pulizia voci

    async def setup_hook(self) -> None: # Metodo che imposta il task checkNews e lo avvia in background
        if debug: print('init pusherNews task')
        self.checkNews.start() # start the task to run in the background - # Avvia il task checkNews, che deve essere definito altrove

    async def on_ready(self): # Metodo chiamato quando il bot si connette a Discord
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=random.randint(MIN_VAL_CHECK_TIME,MAX_VAL_CHECK_TIME))  # decoratore per indicare che verrà eseguita ogni INTERVAL_CHECK_TIME seconds
    
    async def checkNews(self): # definizione della chiamata asincrona ripetuta come indicato sopra
        now = datetime.datetime.now(time_zone).time()
        if debug: print("now is ")
        if debug: print(now)

        #DISCORD
        channel_news = self.get_channel(CANALE_NEWS)  # channel ID chat invio news
        channel_mod = self.get_channel(MOD_ID)  # channel ID chat check funzionamento
        if debug: print('set channel ID done')

        if datetime.datetime.today().weekday() < 7 and start_time <= now <= end_time: #verificare se sabato ok
            delay = random.randint(5, 15) * 60
            if debug: delay = 1

            if debug: print("delay è")
            if debug: print(str(delay)+" secondi")
            time.sleep(delay)

            if debug: print('Starting area loop...')

            for link_area in LINKS_AREA:
                CURRENT_LINK = PRE_LINK + link_area #FOR EACH LINK IN LINKS[]
                if debug: print('CURRENT AREA => '+CURRENT_LINK)
                if debug: print('request...')
                response = requests.get(CURRENT_LINK) #fa una get request ed ottiene l'html della pagina
                response.raise_for_status() #genera eccezione se risponde con errore
                if debug: print('...request done!\n')

                soup = bs4.BeautifulSoup(response.text, 'html.parser') #prende la funzione BeautifulSoup da bs4 che estrae il testo dalla response in formato html(.parser)
                if debug: print('soup is ready! Take and eat, all of you...')

                div_annunci = fix_vision(soup, link_area)

                if debug: print('Finding out all anchor tags...')
                for div_annuncio in reversed(div_annunci): #reversed per rispettare l'ordine di pubblicazione
                    
                    a_annunci = div_annuncio.find_all('a')
                    if debug: print('anchors links loaded!')

                    if debug: print('Matching results...')
                    for a_annuncio in a_annunci:
                        link_annuncio = str(a_annuncio.get('href'))
                        
                        if not link_annuncio.startswith('http'):
                            link_annuncio = PRE_LINK+link_annuncio # AGGIUNGERE FULL PATH - PROBLEMI CON LINK ESTERNI
                        if debug: print('link_annuncio --> '+link_annuncio)
                        titolo_annuncio = a_annuncio.text
                        if debug: print('titolo_annuncio --> '+a_annuncio.text)

                        try:
                            if debug: print('Check if already present...')
                            if link_annuncio in self.values_list or titolo_annuncio in self.values_title_list:
                                print('Already present. Skipped!')
                                
                                # print('CLEANUP DA COMPLETARE)
                                # print('#########')
                                # print('#########')
                                # current_cell = self.tab_correnti.find(link_annuncio, in_column=4)
                                # # print(current_cell.row)
                                # values = self.tab_correnti.row_values(current_cell.row)
                                # empty_row = len(self.tab_archive.col_values(1)) + 1
                                # self.tab_archive.insert_row(values, empty_row)
                                # self.tab_correnti.delete_rows(current_cell.row)
                                # print('#########')
                                # print('#########')
                                # time.sleep(30)

                                # row = cell.row
                                # values = tab_blog.row_values(row)
                                # empty_row = len(tab_archivio.col_values(1)) + 1
                                # tab_archivio.insert_row(values, empty_row)
                                # tab_blog.delete_row(row)
                                # delay(1)

                            else:
                                
                                if debug: print ('\n********CREATE NEW MESSAGE:')
                                nuovo_annuncio = str(get_title(link_area))+'\n'+titolo_annuncio+'\n'+link_annuncio
                                
                                if not TESTINGMODE: await channel_news.send(nuovo_annuncio) # invia su discord

                                # invia su telegram
                                if not TESTINGMODE:
                                    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM_BOT}/sendMessage?chat_id={CHANNEL_CHAT_ID}&text={nuovo_annuncio}"
                                    requests.get(url)

                                if debug: print(nuovo_annuncio+'\n ********\n')
                                
                                # print(self.INDEX)

                                self.sheet.sheet1.insert_row([self.INDEX, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), link_area, link_annuncio, titolo_annuncio, nuovo_annuncio])

                                # self.INDEX = self.INDEX +1 #dumb ma evita rinterrogo GSheet API

                                # RE-READ FILE
                                self.sheet = file.open("pusherNews")  # RE-OPEN

                                self.values_list = self.sheet.sheet1.col_values(4)
                                self.values_title_list = self.sheet.sheet1.col_values(5)
                                self.INDEX = len(self.values_list)
                                if debug: print('sheet has NOW '+str(self.INDEX)+' cols. Set INDEX = '+str(self.INDEX))

                                if debug: print('written into sheet. Now sleep 2 secs')
                                time.sleep(2)
                                if debug: print('Ready! continue into loop...\n')

                            # if debug: print('questo non dovrebbe stamparsi')
                        except Exception as e: print(e)
                    
                    # endfor loop link annunci
                    if debug: print('end loop links')
                # endfor div annunci
                #end for LINKS
                print('All done ;)')

                await channel_mod.send(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' - check') # invia su discord

                    # if autoclose: 
                    #     if not is_mobile: quit()
        else:
            if debug: print("fuori tempo massimo... in attesa orario giusto")
            await channel_mod.send(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' - checkSleep') # invia su discord


    @checkNews.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
