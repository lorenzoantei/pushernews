#!/bin/bash

sudo -u lorenzo DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send "abacScrape - starting new scrape..."
#notify-send ""

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo "current position is "$SCRIPTPATH
cd $SCRIPTPATH

echo "pulizia logs vecchi e check scadenza alert"
find $SCRIPTPATH/logs/* -type f -mmin +$(grep EXPIRE_LOG .env | cut -d "=" -f2 | sed "s/\(.*\)\(--\|#\).*/\1/g") -type f -exec rm -fv {} \; #rimuovi log più vecchi di 7 giorni ~30,20MB
# find temp/ -name checkSixHours -type f -mmin +360 -delete #rimuove checkSix ogni 6 ore

TIMESTAMP=$(date +"%Y%m%d_%H%M")
echo "${TIMESTAMP} - eseguo abacScrape..."
TIMESTAMP=$TIMESTAMP"pusherNews_log"
source dev/bin/activate
/bin/python3 $SCRIPTPATH/pusherNews.py > logs/$TIMESTAMP
sudo -u lorenzo DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send "abacScrape - new scrape done!"
echo "${TIMESTAMP} - abacScrape eseguito"
exit
