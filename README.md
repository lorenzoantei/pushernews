# accademiacarrara.it News scraper
Search for new articles in [accademiacarrara.it/it/segreteria/comunicazioni](https://accademiacarrara.it/it/segreteria/comunicazioni), [accademiacarrara.it/it/blog](https://www.accademiacarrara.it/it/blog), [accademiacarrara.it/it/rassegna-stampa](https://www.accademiacarrara.it/it/rassegna-stampa) and [accademiacarrara.it/it/segreteria/comunicazioni](https://www.accademiacarrara.it/it/segreteria/comunicazioni) and send a notification in our discord network.

## 'DATABASE
Based on:
- GSheet API (https://docs.google.com/spreadsheets/d/1aZWPpD4-JfML9f2gO0t_6X9Xzwe-f5gZO1yA3Z-gKWs/edit#gid=0, sbotsbotsbotsbo@gmail.com)
- [https://docs.gspread.org](gspread Python lib)

## Getting started
Get an Google Account with configurated Google Sheet API as service ( w/ Gcreds.json)
More info:
-  [https://github.com/burnash/gspread](https://github.com/burnash/gspread)
- [https://docs.gspread.org/en/latest/oauth2.html](gspread docs - oauth2)
- [https://console.cloud.google.com](Google Cloud Console)

pip install -r requirements.txt # pip3 freeze > requirements.txt
mv .env.example .env
nano .env
python3 pusherNews.py