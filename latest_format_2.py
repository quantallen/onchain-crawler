from subprocess import list2cmdline
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
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

# Price precision for submitting orders

def pretty_table(dataframe):
    table = PrettyTable(['Ticker', 'Title','Link'])
    table.add_row(dataframe)
    return table
bot = telegram.Bot(token=('5569950433:AAFvCUK4rOpf66O0mPkF-gXtd72Rl9KHIRQ'))
chat_id = '-648351921'
select_Name = {
    'UNI' : 'https://gov.uniswap.org/',
    'APE' :'https://forum.apecoin.com/latest',
    'AAVE' :'https://governance.aave.com/c/governance/4',
    'MKR' :'https://forum.makerdao.com/c/governance/5',
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
}
def _get_snx_url_and_title(Project_Name,day = None):
    
    rs = requests.session()
    req = rs.get(select_Name[Project_Name])
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
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
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
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    driver.implicitly_wait(5)
    driver.get(h[0].find_all('a')[0]['href'])
    find_date = driver.find_element(By.TAG_NAME, 'relative-time').get_attribute('datetime')
    print(find_date)
    datetime_object = datetime.strptime(find_date, '%Y-%m-%dT%H:%M:%SZ')
    driver.quit()
    return datetime_object
def _get_url_and_date(Project_Name,day = None):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)

    driver.get(select_Name[Project_Name])
    '''
    js="var q=document.documentElement.scrollTop=100000"  
    driver.execute_script(js) 
    time.sleep(3)
    '''
    # 执行这段代码，会获取到当前窗口总高度
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
def format_to_gsheet(dataframe):
    scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
                ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        f"{os.path.abspath(os.getcwd())}/goverancesheet.json", scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(
        "1S9N4BBaBS_NtcsomwsGLIQOyn1Qj20OPJIMGSYppCAQ")
    worksheet_list = sheet.worksheets()
    check_list = [t.title for t in worksheet_list]    
    if 'goverance alert formation'not in check_list:
        sheet.add_worksheet(title=f'goverance alert formation', rows=100, cols=30)
        worksheet = sheet.worksheet(f'goverance alert formation')
        dataTitle = ["Ticker", " Title" , "Link"]
        worksheet.append_row(dataTitle,table_range='A1')
    worksheet = sheet.worksheet(f'goverance alert formation')
    worksheet.append_row(dataframe)
    table = pretty_table(dataframe)
    bot.send_message(chat_id= chat_id,text = f'Ticker : {dataframe[0]}\n Title : {dataframe[1]} \n Link : {dataframe[2]}' )
    #text = f'<pre>{table}</pre>', parse_mode=telegram.ParseMode.HTML)
if __name__ =="__main__":
    
    
    PN = ['OHM','YGG','UNI','APE','AAVE','MKR','LDO','CRV','COMP','YFI','ENS'
            ,'ZRX','BAL','BIT','OHM','GmosisDAO','RAD','GTC','API3','ANGLE','SNX']
    #PN = ['GmosisDAO']

    for project_name in PN :
        if project_name == 'OHM':
            list_of_url, list_of_date, list_of_title = _get_ohm_url_and_date(project_name)
            d_u = dict(zip(list_of_date,list_of_url))
            d_f = dict(zip(list_of_date,list_of_title))
            for d in d_u :
                if datetime.now() - d <= timedelta(hours= 3):
                    format_to_gsheet([project_name,d_f[d],d_u[d]])
        elif project_name == 'SNX':
            list_of_url, list_of_title = _get_snx_url_and_title(project_name)
            u_t = dict(zip(list_of_url,list_of_title))
            for u in u_t :
                print('https://sips.synthetix.io'+u+'')
                d = get_date_from_url('https://sips.synthetix.io'+u)
                if datetime.now() - d <= timedelta(hours = 3):
                   format_to_gsheet([project_name,u_t[u],'https://sips.synthetix.io'+u])
        else :
            list_of_url, list_of_date, list_of_title = _get_url_and_date(project_name)
            d_u = dict(zip(list_of_date,list_of_url))
            d_f = dict(zip(list_of_date,list_of_title))
            for d in d_u :
                if datetime.now() - d <= timedelta(hours= 3):
                    format_to_gsheet([project_name,d_f[d],d_u[d]])
                    #all_contents = get_latest_news(d_u[d])

    
    
    
        
