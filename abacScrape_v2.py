#abacScrape v2
debug = 0

import requests, bs4
#from bs4 import BeautifulSoup
from pathlib import Path

# GSHEET API SERVICE LOGIN
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name("sbotsbotsbotsbot_Gcreds.json", scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("pusherNews")  #open sheet

values_list = sheet.sheet1.col_values(3)
INDEX = len(values_list)

PRE_LINK = 'https://accademiacarrara.it'
LINK1 = '/it/blog'
# LINK2 = 'it/rassegna-stampa'
# LINK3 = 'it/news'
# LINK4= 'it/segreteria/comunicazioni'
#LINKS=['it/blog', 'it/rassegna-stampa', 'it/news', 'it/segreteria/comunicazioni']
CURRENT_LINK = PRE_LINK + LINK1 #FOR EACH LINK IN LINKS[]

# logs
Path('logs').mkdir(parents=True, exist_ok=True)
BLOG_LOG = 'logs/blog.csv'
# RASSEGNA_LOG = 'logs/rassegna.csv'
# NEWS = 'logs/segreteria.csv'

response = requests.get(CURRENT_LINK) #fa una get request ed ottiene l'html della pagina
response.raise_for_status() #genera eccezione se risponde con errore

soup=bs4.BeautifulSoup(response.text, 'html.parser') #prende la funzione BeautifulSoup da bs4 che estrae il testo dalla response in formato html(.parser)

old_link_annunci = []
new_link_annunci = []


################################################################
### ANALISI DEI LINK
################################################################

div_annunci=soup.find_all('div', class_='grid-item') #### view-title

for div_annuncio in div_annunci:
    # print(div_annuncio)
    a_annunci = div_annuncio.find_all('a')
    for a_annuncio in a_annunci:
        link_annuncio = PRE_LINK+str(a_annuncio.get('href'))
        if debug: print('prossimo link\n'+link_annuncio+'\n')
        
        try:
            if values_list.index(link_annuncio):
                print('skipped')
        except:
            old_link_annunci.append(link_annuncio)
            new_link_annunci.append(link_annuncio)
            titolo_annuncio = a_annuncio.text
            if titolo_annuncio != 'Leggi':
                print('NUOVOLINK -> '+link_annuncio+'\nTITOLO ANNUNCIO -> '+titolo_annuncio)
                import datetime
                TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.sheet1.insert_row([INDEX, TIMESTAMP, link_annuncio, titolo_annuncio])
                INDEX = INDEX +1  
       
    # endfor loop link annunci
# endfor div annunci

# GSheetListOld.close()

quit()
            
