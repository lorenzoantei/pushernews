

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Impostazione delle credenziali
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sbotsbotsbotsbot_Gcreds.json', scope)
client = gspread.authorize(creds)

# Apertura del documento di Google Sheets
doc = client.open('pusherNews')

# Stampa dei nomi dei fogli di lavoro nel documento
for worksheet in doc.worksheets():
    print(worksheet.title)
