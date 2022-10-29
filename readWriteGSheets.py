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
#print(sheet.sheet1.get('A1'))

values_list = sheet.sheet1.col_values(1)
print(len(values_list))
INDEX = len(values_list)
print(type(INDEX))
# sheet.sheet1.update('A1', 'Bingo!')
#sheet.sheet1.resize(INDEX+1)
# sheet.sheet1.insert_row(['SSS'], index=INDEX+1) # aggiunge in fondo

import datetime
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sheet.sheet1.insert_row([INDEX, TIMESTAMP])

# cell = sheet.sheet1.find("https://accademiacarrara.it/it/blog/donatello-parmi-les-fauves") # PER FARE RICERCHE
quit()

# credits
# https://github.com/burnash/gspread
# https://docs.gspread.org/en/latest/oauth2.html
# https://console.cloud.google.com
# sbotsbotsbotsbo@gmail.com