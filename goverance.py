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
import re
from selenium.webdriver.chrome.service import Service

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
    'BIT':'https://discourse.bitdao.io/latest',
    'OHM':'https://forum.olympusdao.finance/all',
    'GmosisDAO':'https://forum.gnosis.io/c/dao/20/l/latest',
    'RAD':'https://radicle.community/latest',
    'GTC':'https://gov.gitcoin.co/latest',
    'API3':'https://forum.api3.org/',
    'ANGLE':'https://gov.angle.money/latest',
}


def _get_url_and_date(Project_Name,day = None):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

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
        #options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    driver.implicitly_wait(6)
    driver.get(latest_url)
    contents = driver.find_element(By.CLASS_NAME, "cooked").text
    driver.quit()
    print("Contents \n", contents)
    return contents
def get_parser():
    parser = ArgumentParser(description=("This is a script to download historical forem data"),formatter_class=RawTextHelpFormatter)
    parser.add_argument(
      '-n', dest='Project_Name', default= 'AAVE', type= str,help='Project Name to Select')
    parser.add_argument(
        '-l', dest='latest', default= False, help='choose to download latest news')
    parser.add_argument(
        '-d', dest='date', default= None, type = str, help='choose the date range ex: daily , weekly ')
    return parser
def format_to_gsheet(dataframe,date):
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
    if f'{dataframe[0]}_{date}_Analysis' not in check_list:
        sheet.add_worksheet(title=f'{dataframe[0]}_{date}_Analysis', rows=100, cols=30)
        worksheet = sheet.worksheet(f'{dataframe[0]}_{date}_Analysis')
        dataTitle = ["Ticker","Title","Link", "Score"]
        worksheet.append_row(dataTitle,table_range='A1')
    worksheet = sheet.worksheet(f'{dataframe[0]}_{date}_Analysis')
    worksheet.append_row(dataframe)

def trend_analysis(c):
    score = 0
    print(type(c))
    pattern = r'[^A-Za-z0-9]+'
    sample_str = re.sub(pattern, ' ', c)
    sample_str = sample_str.split(' ')
    print(sample_str)
    for s in sample_str :
        if s == 'changes' or s == 'a':
            score += 1
    print("scores :",score)
    return score

if __name__ =="__main__":
    
    
    Project_Name = 'AAVE'
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    
    if args.latest :
        list_of_url, list_of_date, list_of_title = _get_url_and_date(args.Project_Name)
        d_u = dict(zip(list_of_date,list_of_url))
        for d in d_u :
            if datetime.now() - d <= timedelta(hours= 3):
                all_contents = get_latest_news(d_u[d])
                trend_analysis(all_contents)
                
    elif args.date == 'daily': 
        all_contents = []
        list_of_url, list_of_date, list_of_title = _get_url_and_date(args.Project_Name, day = 1)
        d_f = dict(zip(list_of_date,list_of_title))
        d_u = dict(zip(list_of_date,list_of_url))       
        for d in d_u :
            if datetime.now() - d <= timedelta(days= 1):
                all_contents = get_latest_news(d_u[d])
                score = trend_analysis(all_contents)
                format_to_gsheet([args.Project_Name,d_f[d],d_u[d],score],args.date)
        
    elif args.date == 'weekly' :
        all_contents = []
        list_of_url, list_of_date = _get_url_and_date(args.Project_Name, day =7)
        d_u = dict(zip(list_of_date,list_of_url))
        for d in d_u :
            if datetime.now() - d <= timedelta(days= 7):
                all_contents.append(get_latest_news(d_u[d]))
    print(len(all_contents))
    
    
        
