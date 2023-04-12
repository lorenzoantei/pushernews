"""
VARS ENV

EMAIL_SENDER
EMAIL_RECEIVER
PASSWORD

Client_Secret.json

"""

import os
from pathlib import Path
from dotenv import load_dotenv
import unicodedata

def get_variable(var_name: str) -> bool: #semplificazione lettura bools .env
    TRUE_=('true', '1', 't') # Add more entries if you want, like: `y`, `yes`, ...
    FALSE_=('false', '0', 'f')
    value = os.getenv(var_name, 'False').lower()  # return `False` if variable is not set. To raise an error, change `'False'` to `None`
    if value not in TRUE_ + FALSE_:
        raise ValueError(f'Invalid value `{value}` for variable `{var_name}`')
    return value in TRUE_

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
debug = get_variable("DEBUG")
if debug: print("DEBUG MODE\n")



# EMAIL

email = EmailMessage()
email['From'] = os.environ['EMAIL_SENDER']
email['To'] = [os.environ['EMAIL_RECEIVER'] ]
email.set_content(bodyEmail)
if debug: print("setting ssl...")
context = ssl.create_default_context()

sendEmail = get_variable("SEND_EMAIL")
bodyMessageEmail = ""

if debug: print("lessAlert mode ON")
    
def slugify(value, allow_unicode=False): #rende i link filename utilizzabili
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

email['subject'] = "***TITOLO ARTICOLO***"
bodyEmail="***NEW MESSAGE***"

if debug: print("\nprint copy email:\n\n*\n**\n"+bodyEmail+"**\n*\nend body message \n\n")

if bodyEmail:
    if debug: print("connecting SMTP...")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465,) as smtp:
        smtp.login(os.environ['EMAIL_SENDER'], os.environ['PASSWORD'])
        if debug: print("sending emails..")
        smtp.sendmail(os.environ['EMAIL_SENDER'], [os.environ['EMAIL_RECEIVER']], email.as_string())
        if debug: print("emails sent!")

if debug: print("bodyMessage is empty. Nothing to send")