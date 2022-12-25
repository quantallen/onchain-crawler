# -*- coding:UTF-8 -*-


from subprocess import list2cmdline
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from datetime import date, datetime,timedelta
import sys
import time
import os 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import telegram
from prettytable import PrettyTable
import traceback
import pandas as pd
import sqlalchemy
from re import search

#driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

#service = Service(executable_path=ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service)

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user_agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36')

def pretty_table(dataframe):
    table = PrettyTable(['Ticker', 'Title','Link'])
    table.add_row(dataframe)
    return table
bot = telegram.Bot(token=('5783912201:AAHfoRFfruDi4zC58SbKzlmM2aNbe5GFqLQ'))
chat_id = '-1001623977570'
def get_medium_url(url):
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}
    rs = requests.session()
    #req = rs.get(url,headers=user_agent)
    req = rs.get(url,headers=user_agent)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    #title = soup.find_all('div', {'class': 'jc jd je jf jg l'})
    title = soup.find_all('h2', {'class': 'bm gu jj jk jl jm gy jn jo jp jq hc jr js jt ju hg jv jw jx jy hk jz ka kb kc ho hp hq hr ht hv im'})
    print(title)
    #bm gu jj jk jl jm gy jn jo jp jq hc jr js jt ju hg jv jw jx jy hk jz ka kb kc ho hp hq hr ht hv im
    u  = soup.find_all("a",{"class":"au av aw ax ay az ba bb bc bd be bf bg bh bi"})
    list_of_title = []
    for t in title :
        list_of_title.append(t.text)
    list_of_url = []
    for t in u :
        rl = t.get('href')
        list_of_url.append(rl)
    print(list_of_title)
    substring = list_of_title[0].lower().replace(' ','-')
    new_url = ""
    for ur in list_of_url :
        if search(substring, str(ur)):
            new_url = url+ur
            break
    try :
        date_req = rs.get(new_url,headers=user_agent)
        date_req.encoding = 'utf-8'
        soup2 = BeautifulSoup(date_req.text, 'html.parser')
        date = soup2.find_all('p', {'class': 'pw-published-date bm b bn bo cn'})
        year = datetime.today().year
        print(date)
        str_date = str(year)+' '+date[0].text
        datetime_object = datetime.strptime(str_date, '%Y %b %d')
    except :
        return 0, 0,0

        
    return new_url,list_of_title[0], datetime_object
def telegram_send_meg(df):
    t = bot.send_message(chat_id= chat_id,text = f'Ticker : {df[0]}\nTitle : {df[1]} \nLink : {df[2]}\n' )
    print(t)
    time.sleep(1)
def _store_in_db(df,id_ticker_data_dic):
    
    conn = sqlalchemy.create_engine(f'postgresql://datateam:nbolh2n3mfHm@btse-prod-database-datateam-apn1.ccacmtkpnljd.ap-northeast-1.rds.amazonaws.com:5432/datateam')
    _store_data = [[df[2],id_ticker_data_dic[df[0]]]]
    _store_df = pd.DataFrame(_store_data, columns=['link','coin_id'])
    print(_store_df)
    _store_df.to_sql('crypto_news_blog_posts', con=conn,if_exists='append',index=False)
if __name__ =="__main__":
    exist_title = []
    while True :
        start = time.process_time()
        id_ticker_data = pd.read_csv('./id_ticker.csv')
        id_ticker_data_dic = {}
        for i , t in zip(id_ticker_data['id'],id_ticker_data['ticker']):
            id_ticker_data_dic[t]= i
        scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
            ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            f"{os.path.abspath(os.getcwd())}/goverancesheet.json", scope)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(
            "1O2K1ItitG_Qwf7BW4EWkT-5Tvu3Ce7oH_dwZXNyyyFY")
        worksheet = sheet.worksheet('20220915_coin_listing_all')
        df = pd.DataFrame(worksheet.get_all_records())
        newdf = df[df['blog_link'] != '']
        print(len(newdf))
        #newdf= newdf.reset_index()
        newdf = newdf[newdf['ticker'] == 'APT']
        newdf= newdf.reset_index()
        print(newdf)
        for idx,t in enumerate(newdf['blog_link']) :
            print('--------------------------------------')
            print(t)
            url,title,title_date = get_medium_url(t)
            # d_u = dict(zip(list_of_date,list_of_url))
            # d_f = dict(zip(list_of_date,list_of_title))
            # print(len(list_of_url))
            # print(len(list_of_title))
            # print(len(list_of_date))
            print(url, title,title_date)
            if datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) == title_date and url != 0:
                df = [newdf['ticker'][idx],title,url]
                print(df)
                if title not in exist_title :
                        telegram_send_meg(df)
                        _store_in_db(df,id_ticker_data_dic)
                        exist_title.append(title)
        end = time.process_time()
        print("執行時間：%f 秒" % (end - start))
        time.sleep(600)
    