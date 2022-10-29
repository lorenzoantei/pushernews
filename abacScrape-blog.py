import requests, bs4
#from bs4 import BeautifulSoup
from pathlib import Path

PRE_LINK = 'https://accademiacarrara.it/'
LINK1 = 'it/blog'
LINK2 = 'it/rassegna-stampa'
LINK3 = 'it/news'
LINK4= 'it/segreteria/comunicazioni'
#LINKS=['it/blog', 'it/rassegna-stampa', 'it/news', 'it/segreteria/comunicazioni']
CURRENT_LINK = PRE_LINK + LINK1 #FOR EACH LINK IN LINKS[]

# logs
Path('logs').mkdir(parents=True, exist_ok=True)
BLOG_LOG = 'logs/blog.csv'
RASSEGNA_LOG = 'logs/rassegna.csv'
NEWS = 'logs/segreteria.csv'

response = requests.get(CURRENT_LINK) #fa una get request ed ottiene l'html della pagina
response.raise_for_status() #genera eccezione se risponde con errore

soup=bs4.BeautifulSoup(response.text, 'html.parser') #prende la funzione BeautifulSoup da bs4 che estrae il testo dalla response in formato html(.parser)

f = open(BLOG_LOG, 'a')
old_link_annunci = [riga.rstrip('\n') for riga in open(BLOG_LOG)]
new_link_annunci = []

################################################################
### ANALISI DEI LINK
################################################################

div_annunci=soup.find('div', class_='grid') #### view-title
a_annunci=div_annunci.find_all('a')

for a_annuncio in a_annunci:
    link_annuncio = PRE_LINK+str(a_annuncio.get('href'))
    if a_annuncio.text != 'Leggi':
        print(a_annuncio.text)
    
    if link_annuncio not in old_link_annunci:
        f.write('%s\n' % link_annuncio)
        from pprint import pprint
        #pprint(link_annuncio)
        old_link_annunci.append(link_annuncio)
        new_link_annunci.append(link_annuncio)
f.close()

p_annunci=div_annunci.find_all('p')

for p_annuncio in p_annunci:
    print(p_annuncio.text)

if new_link_annunci:
    print('Trovati nuovi annunci!')
    pprint(new_link_annunci)
else:
    print('niente di nuovo')
