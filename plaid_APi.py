
from plaid import Client
import datetime
import json
import os
import psycopg2

client = Client(
  client_id=os.environ.get("CLIENT_ID"),
  secret=os.environ.get("CLIENT_SECRET"),
  environment='development',
  api_version='2019-05-29'  # Specify API version
)

access_token_NAVY=os.environ.get("TOKEN_NAVY")

access_token_AMEX='access-development-3041f26a-ecc4-47c7-9857-f555fa30c704'
access_token_BOFA=os.environ.get("TOKEN_BOFA")


class My_finance():
  connect=psycopg2.connect(user=os.environ.get("USER"),
                          database="plaidapi",
                          password=os.environ.get("PASSWORD_SQL"),
                          host = "127.0.0.1",
                          port = "5432",
                        )


  def __init__(self,token_BOFA,token_NAVY,token_AMEX):
    self.token_BOFA=token_BOFA
    self.token_NAVY=token_NAVY
    self.token_AMEX=token_AMEX



  def get_transactions_AMEX(self):
      start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-360))
      end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
      transactions_response = client.Transactions.get(self.token_AMEX, start_date, end_date)

      return transactions_response

  def get_transactions_BOFA(self):
      start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-360))
      end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
      transactions_response = client.Transactions.get(self.token_BOFA, start_date, end_date)


      return transactions_response

  def get_transactions_NAVY(self):
      start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-360))
      end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
      transactions_response = client.Transactions.get(self.token_NAVY, start_date, end_date)

      return transactions_response

  def update_transactions(self, connect=connect):
    with connect:
      c=connect.cursor()
      for i in self.get_transactions_NAVY()["transactions"]:
        name=i["name"]
        amount=i["amount"]
        date=i["date"]
        merchant_name=i["merchant_name"]
        payment_channel=i['payment_channel']
        account_id=i['account_id']
        category = str(" ".join(i['category']))
        c.execute(''' SELECT EXISTS(SELECT amount FROM transactions WHERE DATE='{}' AND amount='{}' AND category='{}') '''.format(date,amount,category))
        data=c.fetchone()
        if data[0]==False:
          names=i["name"].replace("'","")
          try:
            c.execute("""INSERT INTO transactions (merchant_name,name,category,payment_channel,amount,date,account_id)
                  VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(merchant_name,name,category,payment_channel,amount,date,account_id))
          except psycopg2.errors.StringDataRightTruncation:
            pass


      for i in self.get_transactions_BOFA()["transactions"]:
        name=i["name"]
        amount=i["amount"]
        date=i["date"]
        merchant_name=i["merchant_name"]
        payment_channel=i['payment_channel']
        category = str(" ".join(i['category']))
        account_id=i['account_id']
        c.execute(''' SELECT EXISTS(SELECT amount FROM transactions WHERE DATE='{}' AND amount='{}' AND category='{}') '''.format(date,amount,category))
        data=c.fetchone()
        if data[0]==False:
          if name != None:
            name=i["name"].replace("'","")
          if merchant_name != None:
            merchant_name=i["merchant_name"].replace("'","")
          try:
            c.execute("""INSERT INTO transactions (merchant_name,name,category,payment_channel,amount,date,account_id)
                  VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(merchant_name,name,category,payment_channel,amount,date,account_id))
          except psycopg2.errors.StringDataRightTruncation:
            pass

      for i in self.get_transactions_AMEX()["transactions"]:
        name=i["name"]
        amount=i["amount"]
        date=i["date"]
        merchant_name=i["merchant_name"]
        payment_channel=i['payment_channel']
        category = str(" ".join(i['category']))
        account_id=i['account_id']
        c.execute(''' SELECT EXISTS(SELECT amount FROM transactions WHERE DATE='{}' AND amount='{}' AND category='{}') '''.format(date,amount,category))
        data=c.fetchone()
        if data[0]==False:
          if name != None:
            name=i["name"].replace("'","")
          if merchant_name != None:
            merchant_name=i["merchant_name"].replace("'","")
          try:
            c.execute("""INSERT INTO transactions (merchant_name,name,category,payment_channel,amount,date,account_id)
                  VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(merchant_name,name,category,payment_channel,amount,date,account_id))
          except psycopg2.errors.StringDataRightTruncation:
            pass
      connect.commit()

  def update_amount(self,connect=connect):
    with connect:
      c=connect.cursor()
      for i in self.get_transactions_BOFA()["accounts"]:
          account_id=i['account_id']
          amount=i['balances']['available']
          try:
            c.execute("""update accounts set amount='{}' where id ='{}' """.format(amount,account_id))
          except Exception:
              pass
      for i in self.get_transactions_NAVY()["accounts"]:
          account_id=i['account_id']
          amount=i['balances']['available']
          try:
            c.execute("""update accounts set amount='{}' where id ='{}' """.format(amount,account_id))
          except Exception:
              pass
      for i in self.get_transactions_AMEX()["accounts"]:
          account_id=i['account_id']
          amount=i['balances']['current']
          try:
            c.execute("""update accounts set amount='{}' where id ='{}' """.format(amount,account_id))
          except Exception:
              pass
    connect.commit()



fin=My_finance(access_token_BOFA, access_token_NAVY,access_token_AMEX)
fin.update_transactions()








