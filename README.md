# accademiacarrara.it News scraper
Search for new articles in [accademiacarrara.it/it/segreteria/comunicazioni](https://accademiacarrara.it/it/segreteria/comunicazioni), [accademiacarrara.it/it/blog](https://www.accademiacarrara.it/it/blog), [accademiacarrara.it/it/rassegna-stampa](https://www.accademiacarrara.it/it/rassegna-stampa) and [accademiacarrara.it/it/segreteria/comunicazioni](https://www.accademiacarrara.it/it/segreteria/comunicazioni) and send a notification in our discord network.

## Based on:
- [GSheet API](https://developers.google.com/sheets/api) ('db' at https://docs.google.com/spreadsheets/d/1aZWPpD4-JfML9f2gO0t_6X9Xzwe-f5gZO1yA3Z-gKWs/edit#gid=0)
- [gspread](https://docs.gspread.org), [gspread Github's repo](https://github.com/burnash/gspread)
- [beautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)

## Getting started
Get an Google Account with configurated Google Sheet API as service ( w/ Gcreds.json)
More info:
- 
- [https://docs.gspread.org/en/latest/oauth2.html](gspread docs - oauth2)
- [https://console.cloud.google.com](Google Cloud Console)

`
pip install -r requirements.txt
# or pip install discord python-dotenv requests bs4 oauth2client gspread
mv .env.example .env
nano .env # tune you env
python3 pusherNews.py
`

sbotsbotsbotsbo@gmail.com