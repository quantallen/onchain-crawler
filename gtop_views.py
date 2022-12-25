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
import re
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
chrome_options = Options()
#chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('user_agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36')
select_Name = {
    'UNI' : 'https://gov.uniswap.org/latest?order=views',
    'APE' :'https://forum.apecoin.com/latest?order=views',
    'AAVE' :'https://governance.aave.com/c/governance/4?order=views',
    'MKR' :'https://forum.makerdao.com/c/governance/5?order=views',
    'LDO' :'https://research.lido.fi/latest?order=views',
    'CRV' : 'https://gov.curve.fi/latest?order=views',
    'COMP' :'https://www.comp.xyz/latest?order=views',
    'YFI':'https://gov.yearn.finance/latest?order=views',
    'ENS':'https://discuss.ens.domains/latest?order=views',
    'ZRX':'https://gov.0x.org/latest?order=views',
    'BAL':'https://forum.balancer.fi/latest?order=views',
    'YGG':'https://gov.meritcircle.io/c/governance/2?order=posts',
    'SNX':'https://sips.synthetix.io/all-sip/',
    'BIT':'https://discourse.bitdao.io/latest?order=views',
    'OHM':'https://forum.olympusdao.finance/all',
    'GmosisDAO':'https://forum.gnosis.io/c/dao/20/l/latest?order=views',
    'RAD':'https://gov.gitcoin.co/latest?order=views',
    'GTC':'https://gov.gitcoin.co/latest?order=views',
    'API3':'https://forum.api3.org/latest?order=views',
    'ANGLE':'https://gov.angle.money/latest?order=views',
}
def get_date_from_snx_url(u):
    rs = requests.session()
    req = rs.get(u)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    h = soup.find_all('h1', {'class': 'page-heading'})
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
    driver.implicitly_wait(5)
    driver.get(h[0].find_all('a')[0]['href'])
    find_date = driver.find_element(By.TAG_NAME, 'relative-time').get_attribute('datetime')
    print(find_date)
    datetime_object = datetime.strptime(find_date, '%Y-%m-%dT%H:%M:%SZ')
    driver.quit()
    return datetime_object
# def _get_snx_url_and_title(Project_Name,day = None):
    
#     rs = requests.session()
#     req = rs.get(select_Name[Project_Name])
#     req.encoding = 'utf-8'
#     soup = BeautifulSoup(req.text, 'html.parser')
#     article = soup.find_all('td', {'class': 'sipnum'})
#     title = soup.find_all('td',{'class':'title'})
#     list_of_url = []
#     list_of_title = []
#     for count in range(len(article)):
#         article_url = article[count].find_all('a')[0]['href']
#         list_of_url.append(article_url)
#     for i in range(len(title)):
#         list_of_title.append(title[i].text)
#     return list_of_url, list_of_title
def _get_ohm_url_and_date(Project_Name,day = None):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
    driver.implicitly_wait(5)
    driver.get('https://forum.olympusdao.finance/all?sort=popular')
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
    return list_of_url[:10], list_of_date[:10], list_of_title[:10]
def get_url_sorting_by_views(Project_Name ,day = None):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
    driver.implicitly_wait(5)
    driver.get(select_Name[Project_Name])
    find_href = driver.find_elements(By.CLASS_NAME, "link-top-line")
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
    print(list_of_url)
    print(len(list_of_url))

    driver.quit()
    for t in list_of_timestamp :
        list_of_date.append(datetime.fromtimestamp(int(t)/1000))
    
    return list_of_url[:10], list_of_date[:10], list_of_title[:10]
def _get_url_and_date(Project_Name,day = None):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
    driver.implicitly_wait(5)
    driver.get(select_Name[Project_Name])
    find_href = driver.find_elements(By.CLASS_NAME, "link-top-line")
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
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
        driver.implicitly_wait(6)
        driver.get(u)
        contents = driver.find_element(By.CLASS_NAME, "cooked").text
        all_contents.append(contents)
        driver.quit()
    return all_contents
def get_ohm_news(latest_url):
    list_of_contents = ""
    options = Options()
    option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    #options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(6)
    driver.get(latest_url)
    contents = driver.find_elements(By.CLASS_NAME, "Post-body")
    for content in contents :
            print(content.text)
            list_of_contents += content.text
    driver.quit()
    print("Contents \n", list_of_contents)
    return list_of_contents
def get_latest_news(name, latest_url):
    list_of_contents = ""
    options = Options()
    option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    #options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    driver.implicitly_wait(6)
    driver.get(latest_url)
    if name == 'OHM':
        contents = driver.find_elements(By.CLASS_NAME, "Post-body")
        for content in contents :
            print(content.text)
            list_of_contents += content.text
    elif name == 'SNX':
        contents = driver.find_elements(By.CLASS_NAME, "markdown-content")
        for content in contents :
            print(content.text)
            list_of_contents += content.text
    else :
        contents = driver.find_elements(By.CLASS_NAME, "cooked")
        print(contents)
        for content in contents :
            print(content.text)
            list_of_contents += content.text
        #.text
        
    driver.quit()
    print("Contents \n", list_of_contents)
    return list_of_contents
def get_parser():
    parser = ArgumentParser(description=("This is a script to download historical forem data"),formatter_class=RawTextHelpFormatter)
    parser.add_argument(
      '-n', dest='Project_Name', default= 'AAVE', type= str,help='Project Name to Select')
    parser.add_argument(
        '-l', dest='latest', default= False, help='choose to download latest news')
    parser.add_argument(
        '-d', dest='date', default= None, type = str, help='choose the date range ex: daily , weekly ')
    return parser

def format_to_gsheet(dataframe,sheet):
    worksheet_list = sheet.worksheets()
    check_list = [t.title for t in worksheet_list]    
    if f'{dataframe[0]}_Top10Views_Analysis' not in check_list:
        sheet.add_worksheet(title=f'{dataframe[0]}_Top10Views_Analysis', rows=100, cols=30)
        worksheet = sheet.worksheet(f'{dataframe[0]}_Top10Views_Analysis')
        dataTitle = ["Ticker","Rank","Title", "Link"]
        worksheet.append_row(dataTitle,table_range='A1')
    worksheet = sheet.worksheet(f'{dataframe[0]}_Top10Views_Analysis')
    worksheet.append_row(dataframe)
def clear_gsheet(sheet):
    worksheets = sheet.worksheets()
    reqs = [{"addSheet": {"properties": {"index": 0}}}] + [{"deleteSheet": {"sheetId": s.id}} for s in worksheets]
    sheet.batch_update({"requests": reqs})
def trend_analysis(c):
    score = 0
    print(type(c))
    pattern = r'[^A-Za-z0-9]+'
    sample_str = re.sub(pattern, ' ', c)
    sample_str = sample_str.split(' ')
    print(sample_str)
    for s in sample_str :
        if s.lower() == 'buy' or s.lower() == 'buyback':
            score += 1
    print("scores :",score)
    return score
def views_sorting(name,day,sheet,str_date):
    if name == 'OHM':
            list_of_url, list_of_date, list_of_title = _get_ohm_url_and_date(name)
            d_u = dict(zip(list_of_date,list_of_url))
            d_f = dict(zip(list_of_date,list_of_title))
            for rank , d in enumerate(d_f):
                format_to_gsheet([name,rank+1,d_f[d],d_u[d]],sheet)
    else :
        list_of_url, list_of_date, list_of_title = get_url_sorting_by_views(name, day = day)
        d_f = dict(zip(list_of_date,list_of_title))
        d_u = dict(zip(list_of_date,list_of_url))  
        for rank , d in enumerate(d_f):
            format_to_gsheet([name,rank+1,d_f[d],d_u[d]],sheet)
            time.sleep(2)

def news_analysis(name,day,str_date):
    all_contents = []
    if name == 'OHM':
            list_of_url, list_of_date, list_of_title = _get_ohm_url_and_date(name)
            d_u = dict(zip(list_of_date,list_of_url))
            d_f = dict(zip(list_of_date,list_of_title))
            for d in d_u :
                if datetime.now() - d <= timedelta(days = day):
                    all_contents = get_ohm_news(d_u[d])
                    score = trend_analysis(all_contents)
                    format_to_gsheet([name,d_f[d],d_u[d],score],str_date)
    # elif name == 'SNX':
    #     list_of_url, list_of_title = _get_snx_url_and_title(name)
    #     u_t = dict(zip(list_of_url,list_of_title))
    #     for u in u_t :
    #         print('https://sips.synthetix.io'+u+'')
    #         d = get_date_from_snx_url('https://sips.synthetix.io'+u)
    #         if datetime.now() - d <= timedelta(days = day):
    #             all_contents = get_latest_news(name,'https://sips.synthetix.io'+u)
    #             score = trend_analysis(all_contents)
    #             format_to_gsheet([name,u_t[u],'https://sips.synthetix.io'+u,score],str_date)
    else :
        list_of_url, list_of_date, list_of_title = _get_url_and_date(name, day = day)
        d_f = dict(zip(list_of_date,list_of_title))
        d_u = dict(zip(list_of_date,list_of_url))  
        for d in d_u :
            if datetime.now() - d <= timedelta(days= 1):
                all_contents = get_latest_news(name,d_u[d])
                score = trend_analysis(all_contents)
                format_to_gsheet([name,d_f[d],d_u[d],score],str_date)
if __name__ =="__main__":
    
    
    
    PN = ['OHM','YGG','UNI','APE','AAVE','MKR','LDO','COMP','YFI','ENS'
            ,'ZRX','BAL','BIT','GmosisDAO','RAD','GTC','API3','ANGLE','CRV']
    #PN = ['UNI']
    while True :
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
                ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            f"{os.path.abspath(os.getcwd())}/goverancetopviews.json", scope)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(
            "1xUZry0oRJh6LJmLFOyC9dlsJDdoloWF-F8wJ4FpDaqw")
        clear_gsheet(sheet)
        for pn in PN :
            views_sorting(pn,1,sheet,'daily')
        time.sleep(86400)
        
    
    