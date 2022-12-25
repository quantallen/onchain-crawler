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
from datetime import datetime
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
    'YGG':'https://gov.meritcircle.io/',
    'SNX':'https://sips.synthetix.io/all-sip/',
    'BIT':'https://discourse.bitdao.io/latest',
    'OHM':'https://forum.olympusdao.finance/all',
    'GmosisDAO':'https://forum.gnosis.io/c/dao/20/l/latest',
    'RAD':'https://radicle.community/latest',
    'GTC':'https://gov.gitcoin.co/latest',
    'API3':'https://forum.api3.org/',
    'ANGLE':'https://gov.angle.money/latest',
}

def _get_url_and_date(Project_Name,day = None):
    
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
def get_date_from_url(u):
    rs = requests.session()
    req = rs.get(u)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    h = soup.find_all('h1', {'class': 'page-heading'})
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(6)
    driver.get(h[0].find_all('a')[0]['href'])
    find_date = driver.find_element(By.TAG_NAME, 'relative-time').get_attribute('datetime')
    print(find_date)
    datetime_object = datetime.strptime(find_date, '%Y-%m-%dT%H:%M:%SZ')
    driver.quit()
    return datetime_object

def get_comtents_of_url(list_of_url):
    all_contents = []
    for u in list_of_url :
        options = Options()
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
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
    option.add_argument('headless')
    #options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    driver.implicitly_wait(6)
    driver.get(latest_url)
    contents = driver.find_element(By.CLASS_NAME, "cooked").text
    driver.quit()
    print("Contents \n", contents)

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
if __name__ =="__main__":
    
    
    PN = ['SNX']

    for project_name in PN :
        if project_name != 'OHM':
            list_of_url, list_of_title = _get_url_and_date(project_name)

            u_t = dict(zip(list_of_url,list_of_title))
            for u in u_t :
                print('https://sips.synthetix.io'+u+'')
                d = get_date_from_url('https://sips.synthetix.io'+u)
                if datetime.now() - d <= timedelta(days=7):
                   format_to_gsheet([project_name,u_t[u],'https://sips.synthetix.io'+u])
        

    
    
    
    # https://sips.synthetix.io/sips/sip-8/    
