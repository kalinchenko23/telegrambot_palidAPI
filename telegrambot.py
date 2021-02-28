import telebot
import time
import requests
import json
import os
from plaid_APi import fin
from  expenses_SQL_pandas import df
import logging


#setting up logging settings
logger=logging.getLogger(__name__)
file_handler=logging.FileHandler('new_plaid.log')
logger.addHandler(file_handler)
formatter=logging.Formatter('%(asctime)s:%(levelno)s:%(message)s:%(module)s:%(funcName)s')
file_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)



bot_token=os.environ.get("BOT_TOKEN")



class Telegram_bot():
    def __init__(self,token):
        self.token=bot_token
        self.base=f"https://api.telegram.org/bot{self.token}"


    def get_updates(self, offset=None):


        url=self.base+"/getUpdates?timeout=100"

        if offset:
            url=url+f"&offset={offset+1}"
        r=requests.get(url)
        return json.loads(r.content)
    def send_message(self, msg,chat_id):
        url=self.base+f"/sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)


update_id=None
bot=Telegram_bot(bot_token)

def make_reply(msg):
    if msg=="help".lower():
        reply="""Here is your options:\n\"total\" for total amount on the bank account\n\"transactions\" for all transactions for the week
        \n\"weekly\" for total spending of the week\n\"monthly\" for total spending of the month"""

    elif "total" in msg.lower():
       	reply=df.current_fin_state()

    elif "transactions" in msg.lower():
        reply=df.weekly_transactions()

    elif "weekly" in msg.lower():
        reply= df.weekly_analysis()

    elif "monthly" in msg.lower():
        reply= df.monthly_analysis()



    else:
        reply="ok"
    return reply

while True:
    updates=bot.get_updates(offset=update_id)
    updates=updates["result"]

    if updates:

        for i in updates:

            update_id=i["update_id"]
            try:
                message=i["message"]["text"]
            except:
                message=None


            from_=i["message"]["from"]["id"]
            reply=make_reply(message)
            logger.info(message)
            bot.send_message(reply,from_)











