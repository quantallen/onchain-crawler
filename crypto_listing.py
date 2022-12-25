from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
from re import sub
from decimal import Decimal
from selenium.webdriver.common.action_chains import ActionChains  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


options = webdriver.ChromeOptions()
options.add_experimental_option('extensionLoadTimeout', 60000)
chrome_options = Options()
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')
#chrome_options.add_argument('--disable-dev-shm-usage')
options.add_argument('user_agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(6)
from datetime import datetime
def spot(exchange):
    driver.get(f'https://coinmarketcap.com/exchanges/{exchange}')
    #wait = WebDriverWait(driver, 10)
    time.sleep(3)
    js="var q=document.documentElement.scrollTop=100000"  
    driver.execute_script(js) 
    time.sleep(3)
    '''
    '''
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    # new_height = driver.execute_script(js)
    # while height < new_height :
    #     # 将滚动条调整至页面底部
    #     for i in range(height, new_height, 500):
    #         driver.execute_script('window.scrollTo(0, {})'.format(i))
    #         time.sleep(0.5)
    #     height = new_height
    #     time.sleep(2)
    #     new_height = driver.execute_script(js)
    try :
        l =driver.find_element(By.CLASS_NAME,"cmc-cookie-policy-banner__close")
        time.sleep(0.5)
        actions  = ActionChains(driver)
        actions.move_to_element(l)
        actions.click(l)
        actions.perform()
    except :
        pass
    

    while True :
        try :
            l =driver.find_element(By.CLASS_NAME,"x0o17e-0.DChGS.d6bmin-11.fWsPbo")
            print("load more :",l)
            time.sleep(0.5)
            actions  = ActionChains(driver)
            actions.move_to_element(l)
            actions.click(l)
            actions.perform()
            #l.click()
            time.sleep(0.5)
        except :
            break
    # l =driver.find_element(By.CLASS_NAME,"sc-1eb5slv-0.iKUzJY")
    # l.click()
    # find_href = driver.find_elements(By.CLASS_NAME, "sc-1eb5slv-0.iKUzJY")
    # find_href[6].click()
    html = driver.page_source
    soup = BeautifulSoup(html)
    coins = soup.find_all('a', {'class': 'sc-130rhjl-0 kLuYhf cmc-link'})
    volume = soup.find_all('p', {'class': 'sc-1eb5slv-0 eWvSno'})
    currency = soup.find_all('div',{'class':'sc-16r8icm-0 sc-1teo54s-1 dNOTPP'})
    dic = {}
    new_volume = [v for idx,v in enumerate(volume) if idx % 5 == 1]
    for c, v ,cu in zip(coins,new_volume,currency):
        dic[c.text] = [v.text,cu.text]
    # if exchange == 'Binance':
    #d = {k.split('/')[0]: v for k, v in dic.items() if k.split('/')[1] == 'USDT'}
    #d = {k.split('/')[0]:[v,c] for k, [v,c] in dic.items() if k.split('/')[1] == 'WETH'}
    d = {k.split('/')[0]:[v,c] for k, [v,c] in dic.items() if k.split('/')[1] == 'USDT'}
    count = 0
    new_d = {}
    return d
def dex(exchange):
    driver.get(f'https://coinmarketcap.com/exchanges/{exchange}')
    #wait = WebDriverWait(driver, 10)
    time.sleep(3)
    js="var q=document.documentElement.scrollTop=100000"  
    driver.execute_script(js) 
    time.sleep(3)
    '''
    '''
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    # new_height = driver.execute_script(js)
    # while height < new_height :
    #     # 将滚动条调整至页面底部
    #     for i in range(height, new_height, 500):
    #         driver.execute_script('window.scrollTo(0, {})'.format(i))
    #         time.sleep(0.5)
    #     height = new_height
    #     time.sleep(2)
    #     new_height = driver.execute_script(js)
    try :
        l =driver.find_element(By.CLASS_NAME,"cmc-cookie-policy-banner__close")
        time.sleep(0.5)
        actions  = ActionChains(driver)
        actions.move_to_element(l)
        actions.click(l)
        actions.perform()
    except :
        pass
    

    while True :
        try :
            l =driver.find_element(By.CLASS_NAME,"x0o17e-0.DChGS.d6bmin-11.fWsPbo")
            print("load more :",l)
            time.sleep(0.5)
            actions  = ActionChains(driver)
            actions.move_to_element(l)
            actions.click(l)
            actions.perform()
            #l.click()
            time.sleep(0.5)
        except :
            break
    # l =driver.find_element(By.CLASS_NAME,"sc-1eb5slv-0.iKUzJY")
    # l.click()
    # find_href = driver.find_elements(By.CLASS_NAME, "sc-1eb5slv-0.iKUzJY")
    # find_href[6].click()
    html = driver.page_source
    soup = BeautifulSoup(html)
    coins = soup.find_all('a', {'class': 'sc-130rhjl-0 kLuYhf cmc-link'})
    volume = soup.find_all('p', {'class': 'sc-1eb5slv-0 eWvSno'})
    currency = soup.find_all('div',{'class':'sc-16r8icm-0 sc-1teo54s-1 dNOTPP'})
    dic = {}
    new_volume = [v for idx,v in enumerate(volume) if idx % 5 == 1]
    for c, v ,cu in zip(coins,new_volume,currency):
        dic[c.text] = [v.text,cu.text]
    # if exchange == 'Binance':
    #d = {k.split('/')[0]: v for k, v in dic.items() if k.split('/')[1] == 'USDT'}
    d = {k.split('/')[0]:[v,c] for k, [v,c] in dic.items() if k.split('/')[1] == 'WETH'}
    #d = {k.split('/')[0]:[v,c] for k, [v,c] in dic.items() if k.split('/')[1] == 'USDT'}
    # count = 0
    # new_d = {}
    # for k,[v,c] in d.items():
    #     if count < 10 :
    #         new_d[k] = [v,c]
    #         count += 1
    #     d = {k.split('/')[0]: v for k, v in dic.items() if k.split('/')[1] == 'USD'}
    return d
def get_forum_url(currency):
    print("currency", currency)
    currency= currency.lower()
    currency =currency.replace(' ','-')
    currency =currency.replace('.','-')
    driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver2.implicitly_wait(6)

    driver2.get(f'https://coinmarketcap.com/currencies/{currency}/')
    t = driver2.find_elements(By.CLASS_NAME,"sc-16r8icm-0.coGWQa")
    #print(t)
    try :
        ActionChains(driver2).move_to_element(t[4]).perform()
    except :
        return ''
    find_href = driver2.find_elements(By.LINK_TEXT, "medium.com")
    
    #print(find_href)
    try :
        find_href[0].click()
    except :
        return ''
    driver2.switch_to.window(driver2.window_handles[-1])

    url = driver2.current_url
    driver2.quit()
    return url

def format_to_gsheet(dataframe,sheet):
    
    worksheet_list = sheet.worksheets()
    check_list = [t.title for t in worksheet_list]    
    name = f'{datetime.now().date().strftime("%Y%m%d")}_coin_listing_all'#-{exchange}'
    if name not in check_list:
        sheet.add_worksheet(title=name, rows=100, cols=30)
        worksheet = sheet.worksheet(name)
        dataTitle = ["Symbol","Volume","Link"]
        
        worksheet.append_row(dataTitle,table_range='A1')
    else :
        worksheet = sheet.worksheet(name)
        worksheet.clear()
        dataTitle = ["Symbol","Volume","Link"]          
        worksheet.append_row(dataTitle,table_range='A1')
    for df in dataframe :
        time.sleep(1)
        worksheet.append_row(df)

if __name__ == "__main__":
    list_of_coin = []
    spot_exchanges = ['coinbase-exchange','binance','ftx','kucoin','huobi']
    #spot_exchanges = ['coinbase-exchange']
    dex_exchanges = ['uniswap-v3','uniswap-v2']
    #dex_exchanges = []
    #dex_exchanges = ['uniswap-v3']
    #exchanges = ['coinbase-exchange']
    for e in spot_exchanges :
        data = spot(e)
        print(len(data))
        list_of_coin.append(data)
        print(data)
    for e in dex_exchanges :
        data = dex(e)
        print(data)
        list_of_coin.append(data)
    dic ={}
    df = []
    for data in list_of_coin :
        for k, [v,c] in data.items():
            #print(k,v,c)
            if k not in dic:
                #df.append([k,v])
                dic[k] = [v,c] 
            else :
                #Decimal(sub(r'[^\d.]', '', df[k]))
                #print(df[k],)
                #print("Compare :",Decimal(sub(r'[^\d.]', '', dic[k][0])),Decimal(sub(r'[^\d.]', '', v)))
                if Decimal(sub(r'[^\d.]', '', dic[k][0])) <= Decimal(sub(r'[^\d.]', '', v)):
                    #print("Compare :",Decimal(sub(r'[^\d.]', '', dic[k][0])),Decimal(sub(r'[^\d.]', '', v)))
                    dic[k] = [v,c]
    for k,[v,c]in dic.items():
        #df.append([k,v,c])
        df.append([k,v,get_forum_url(c)])
    df.sort(key= lambda x : Decimal(sub(r'[^\d.]', '', x[1])),reverse=True)
    print(df)
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
        ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        f"{os.path.abspath(os.getcwd())}/goverancesheet.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(
        "1O2K1ItitG_Qwf7BW4EWkT-5Tvu3Ce7oH_dwZXNyyyFY")
    format_to_gsheet(df,sheet)