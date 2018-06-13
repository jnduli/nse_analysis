cd "$(dirname "$0")"
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

RUNSCRIPT="/run.sh"
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH$RUNSCRIPT

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/30 9-15 * * * $SCRIPTPATH$RUNSCRIPT" >> mycron
#install new cron file
crontab mycron
