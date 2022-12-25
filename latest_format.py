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
import sqlalchemy
import pandas as pd
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
#hrome_options.add_argument("--start-maximized")
#chrome_options.add_argument('--ignore-certificate-errors')
#chrome_options.add_argument("--proxy-bypass-list=*")
#chrome_options.add_argument("--proxy-server='direct://'")
#chrome_options.add_argument("--disable-extensions")


# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument("--log-level=3")
# chrome_options.add_argument('start-maximized')
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument('disable-infobars')
#chrome_options.add_argument('disable-blink-features=AutomationControlled')
#chrome_options.add_argument('user-agent=Type user agent here')
def pretty_table(dataframe):
    table = PrettyTable(['Ticker', 'Title','Link'])
    table.add_row(dataframe)
    return table
bot = telegram.Bot(token=('5569950433:AAFvCUK4rOpf66O0mPkF-gXtd72Rl9KHIRQ'))
chat_id = '-1001751306561'
select_Name = {
    'UNI' : 'https://gov.uniswap.org/',
    'APE' :'https://forum.apecoin.com/latest',
    'AAVE' :'https://governance.aave.com/c/governance/4',
    'MKR' :'https://forum.makerdao.com/latest',
    'LDO' :'https://research.lido.fi/',
    'CRV' : 'https://gov.curve.fi/latest',
    'COMP' :'https://www.comp.xyz/latest',
    'YFI':'https://gov.yearn.finance/latest',
    'ENS':'https://discuss.ens.domains/latest',
    'ZRX':'https://gov.0x.org/',
    'BAL':'https://forum.balancer.fi/latest',
    'YGG':'https://gov.meritcircle.io/c/governance/2',
    'SNX':'https://sips.synthetix.io/all-sip/',
    'BIT':'https://discourse.bitdao.io/latest',
    'OHM':'https://forum.olympusdao.finance/all',
    'GmosisDAO':'https://forum.gnosis.io/c/dao/20/l/latest',
    'RAD':'https://radicle.community/latest',
    'GTC':'https://gov.gitcoin.co/latest',
    'API3':'https://forum.api3.org/',
    'ANGLE':'https://gov.angle.money/latest',
    'Jpegd':'https://gov.jpegd.io/latest',
    'Benddao':'https://governance.benddao.xyz/',
    'LUNA':'https://agora.terra.money/discussions/2.%20Governance%20and%20Proposals'
}
def _get_luna_url_and_title(Project_Name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
    
    driver.get('https://agora.terra.money/discussions/2.%20Governance%20and%20Proposals')
    driver.implicitly_wait(5)
    #print(find_date)
    list_of_url = []
    list_of_date = []
    list_of_title = []
    find_href = driver.find_elements(by=By.CSS_SELECTOR, value=".last-active.created-at")
    
    find_date = driver.find_elements(By.CLASS_NAME, "last-active.created-at")

    for link in find_href:
        a = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
        list_of_url.append(a)
    find_title = driver.find_elements(By.CLASS_NAME,"row-header")
    for d in find_date:
        tmp = d.text
        data = tmp.split(' ')
        list_of_date.append(data[-2])
    #print(find_title)
    for t in find_title:
        list_of_title.append(t.text)
    driver.quit()
    return list_of_url, list_of_date, list_of_title

def _get_snx_url_and_title(Project_Name,day = None):
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}
    rs = requests.session()
    req = rs.get(select_Name[Project_Name],headers=user_agent)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    article = soup.find_all('td', {'class': 'sipnum'})
    title = soup.find_all('td',{'class':'title'})
    list_of_url = []
    list_of_title = []
    for count in range(len(article)):
        article_url = article[count].find_all('a')[0]['href']
        list_of_url.append(article_url)
    for i in range(len(title)):
        list_of_title.append(title[i].text)
    return list_of_url, list_of_title
def _get_ohm_url_and_date(Project_Name,day = None):
    # /usr/bin/google-chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
    #driver = webdriver.Chrome(options = chrome_options)
    driver.implicitly_wait(5)
    driver.get('https://forum.olympusdao.finance/all')
    find_date = driver.find_elements(By.CLASS_NAME, "item-terminalPost")
    #print(find_date)
    list_of_url = []
    list_of_date = []
    list_of_title = []
    find_href = driver.find_elements(By.CLASS_NAME, "DiscussionListItem-main")

    for link in find_href:
        #a = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
        a = link.get_attribute('href')
        list_of_url.append(a)
        title = link.get_attribute('textContent')
        list_of_title.append(title)
    for link in find_date:
        a = link.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
        date = datetime.strptime(a, '%Y-%m-%dT%H:%M:%S%z')
        date = date.replace(tzinfo=None) 
        list_of_date.append(date)
    driver.quit()
    return list_of_url, list_of_date, list_of_title
def get_date_from_url(u):
    rs = requests.session()
    req = rs.get(u)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    h = soup.find_all('h1', {'class': 'page-heading'})
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(h[0].find_all('a')[0]['href'])
    find_date = driver.find_element(By.TAG_NAME, 'relative-time').get_attribute('datetime')
    print(find_date)
    datetime_object = datetime.strptime(find_date, '%Y-%m-%dT%H:%M:%SZ')
    driver.quit()
    return datetime_object
def _get_url_and_date(Project_Name,day = None):
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
    #driver = webdriver.Chrome(options = chrome_options)
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(6)
    driver.get(select_Name[Project_Name])
    '''
    js="var q=document.documentElement.scrollTop=100000"  
    driver.execute_script(js) 
    time.sleep(3)
    '''
    '''
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    new_height = driver.execute_script(js)
    while height < new_height and day:
        check_date = driver.find_elements(By.CLASS_NAME, "post-activity")
        cd = check_date[-1].find_element(By.TAG_NAME, 'span').get_attribute('data-time')
        if datetime.now() - datetime.fromtimestamp(int(cd)/1000) >= timedelta(days = day):
            break
        # 将滚动条调整至页面底部
        for i in range(height, new_height, 100):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.5)
        height = new_height
        time.sleep(2)
        new_height = driver.execute_script(js)
    '''
    driver.implicitly_wait(5)
    find_href = driver.find_elements(By.CLASS_NAME, "link-top-line")
    
    print(find_href)
    find_date = driver.find_elements(By.CLASS_NAME, "post-activity")
    list_of_url = []
    list_of_timestamp = []
    list_of_date = []
    list_of_title = []
    for link in find_href:
        a = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
        title = link.find_element(By.TAG_NAME, 'a').get_attribute("textContent")
        list_of_url.append(a)
        list_of_title.append(title)
    for link in find_date:
        a = link.find_element(By.TAG_NAME, 'span').get_attribute('data-time')
        list_of_timestamp.append(a)
    print(len(list_of_url))
    print(list_of_timestamp)
    

    driver.quit()
    for t in list_of_timestamp :
        list_of_date.append(datetime.fromtimestamp(int(t)/1000))
    
    return list_of_url, list_of_date, list_of_title

def get_comtents_of_url(list_of_url):
    all_contents = []
    for u in list_of_url :
        options = Options()
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
        driver.implicitly_wait(6)
        driver.get(u)
        contents = driver.find_element(By.CLASS_NAME, "cooked").text
        all_contents.append(contents)
        driver.quit()
    return all_contents

def get_latest_news(latest_url):
    options = Options()
    option = webdriver.ChromeOptions()
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    driver.implicitly_wait(6)
    driver.get(latest_url)
    contents = driver.find_element(By.CLASS_NAME, "cooked").text
    driver.quit()
    print("Contents \n", contents)
def get_parser():
    parser = ArgumentParser(description=("This is a script to download historical forem data"),formatter_class=RawTextHelpFormatter)
    parser.add_argument(
      '-n', dest='Project_Name', default= 'AAVE', type= str,help='Project Name to Select')
    parser.add_argument(
        '-l', dest='latest', default= False, help='choose to download latest news')
    parser.add_argument(
        '-d', dest='date', default= None, type = str, help='choose the date range ex: daily , weekly ')
    return parser
def telegram_send_meg(df):
    t = bot.send_message(chat_id= chat_id,text = f'Ticker : {df[0]}\nTitle : {df[1]} \nLink : {df[2]}' )
    print(t)
    time.sleep(1)
def format_to_gsheet(dataframe,sheet):
    
    worksheet_list = sheet.worksheets()
    check_list = [t.title for t in worksheet_list]    
    if 'goverance alert formation'not in check_list:
        sheet.add_worksheet(title=f'goverance alert formation', rows=100, cols=30)
        worksheet = sheet.worksheet(f'goverance alert formation')
        dataTitle = ["Ticker", " Title" , "Link"]
        worksheet.append_row(dataTitle,table_range='A1')
    else :
        worksheet = sheet.worksheet(f'goverance alert formation')
        worksheet.clear()
        dataTitle = ["Ticker", " Title" , "Link"]
        worksheet.append_row(dataTitle,table_range='A1')
    for df in dataframe :
        worksheet.append_row(df)
        table = pretty_table(df)

def _store_in_db(df,id_ticker_data_dic):
    
    conn = sqlalchemy.create_engine(f'postgresql://datateam:nbolh2n3mfHm@btse-prod-database-datateam-apn1.ccacmtkpnljd.ap-northeast-1.rds.amazonaws.com:5432/datateam')
    _store_data = [[df[2],id_ticker_data_dic[df[0]]]]
    _store_df = pd.DataFrame(_store_data, columns=['link','coin_id'])
    print(_store_df)
    _store_df.to_sql('crypto_news_goverance_posts', con=conn,if_exists='append',index=False)
    
if __name__ =="__main__":
    exist_title = []
    while True :
        try :
            start = time.process_time()
            id_ticker_data = pd.read_csv('./id_ticker.csv')
            id_ticker_data_dic = {}
            for i , t in zip(id_ticker_data['id'],id_ticker_data['ticker']):
                id_ticker_data_dic[t]= i
            PN = ['UNI','APE','AAVE','MKR','LDO','COMP','YFI','ENS'
                    ,'ZRX','BAL','BIT','OHM','GmosisDAO','YGG','RAD','GTC','API3','ANGLE','SNX','CRV','Benddao','Jpegd','LUNA']
            #PN = ['GmosisDAO']
            #PN = ['APE']
            #PN = ['ENS']
            scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive'
                        ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                f"{os.path.abspath(os.getcwd())}/goverancesheet.json", scope)
            client = gspread.authorize(credentials)

            sheet = client.open_by_key(
                "1S9N4BBaBS_NtcsomwsGLIQOyn1Qj20OPJIMGSYppCAQ")
            post_dataframe = []

            for project_name in PN :
                print("project_name  :", project_name)
                if project_name == 'OHM':
                    list_of_url, list_of_date, list_of_title = _get_ohm_url_and_date(project_name)
                    d_u = dict(zip(list_of_date,list_of_url))
                    d_f = dict(zip(list_of_date,list_of_title))
                    for d in d_u :
                        if datetime.now() - d <= timedelta(minutes= 3):
                            df = [project_name,d_f[d],d_u[d]]
                            post_dataframe.append(df)
                            if d_f[d] not in exist_title :
                                telegram_send_meg(df)
                                _store_in_db(df,id_ticker_data_dic)
                                exist_title.append(d_f[d])
                            #format_to_gsheet([project_name,d_f[d],d_u[d]])
                elif project_name == 'SNX':
                    list_of_url, list_of_title = _get_snx_url_and_title(project_name)
                    u_t = dict(zip(list_of_url,list_of_title))
                    for u in u_t :
                        print('https://sips.synthetix.io'+u+'')
                        d = get_date_from_url('https://sips.synthetix.io'+u)
                        if datetime.now() - d <= timedelta(minutes= 3):
                            df = [project_name,u_t[u],'https://sips.synthetix.io'+u]
                            post_dataframe.append(df)
                            if u_t[u] not in exist_title :
                                telegram_send_meg(df)
                                _store_in_db(df,id_ticker_data_dic)
                                exist_title.append(u_t[u])
                elif project_name == 'LUNA':
                    list_of_url, list_of_date, list_of_title = _get_luna_url_and_title(project_name)
                    d_u = dict(zip(list_of_date,list_of_url))
                    d_f = dict(zip(list_of_date,list_of_title))
                    for d in d_u :
                        if d == '1m' or d == '1min' or d == '1mins':
                            df = [project_name,d_f[d],d_u[d]]
                            post_dataframe.append(df)
                            if d_f[d] not in exist_title :
                                telegram_send_meg(df)
                                _store_in_db(df,id_ticker_data_dic)
                                exist_title.append(d_f[d])

                else :
                    list_of_url, list_of_date, list_of_title = _get_url_and_date(project_name)
                    d_u = dict(zip(list_of_date,list_of_url))
                    d_f = dict(zip(list_of_date,list_of_title))
                    for d in d_u :
                        if datetime.now() - d <= timedelta(minutes= 3):
                            df = [project_name,d_f[d],d_u[d]]
                            post_dataframe.append(df)
                            if d_f[d] not in exist_title :
                                print("in")
                                telegram_send_meg(df)
                                _store_in_db(df,id_ticker_data_dic)
                                exist_title.append(d_f[d])
                            #all_contents = get_latest_news(d_u[d])
            print("exist title :", exist_title)
            #format_to_gsheet(post_dataframe,sheet)
            end = time.process_time()
            print("執行時間：%f 秒" % (end - start))
            time.sleep(60)
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(10)
            continue
    
    
    
        
