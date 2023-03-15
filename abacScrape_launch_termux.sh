#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo "current position is "$SCRIPTPATH
cd $SCRIPTPATH

echo "pulizia logs vecchi e check scadenza alert"
find $SCRIPTPATH/logs/* -type f -mmin +10080 -type f -exec rm -fv {} \; #rimuovi log più vecchi di 7 giorni

TIMESTAMP=$(date +"%Y%m%d_%H%M")
# echo "${TIMESTAMP} - eseguo abacScrape..."
TIMESTAMP=$TIMESTAMP"pusherNews_log"
/bin/python $SCRIPTPATH/pusherNews.py > $SCRIPTPATH/logs/$TIMESTAMP

# echo "${TIMESTAMP} - abacScrape eseguito"
exit
