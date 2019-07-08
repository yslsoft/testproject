from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def html(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', class_='chargeItemWrp')
    return table

def remove_ws(str):
    return ' '.join(str.replace('\n\n','').replace('\t','').strip('\n ').split())

def getList():
    try:
        table = html(driver)
        divs = table.find_all('div', class_='charge_box')
        for div in divs:
            valueList = ['','','','','']
            valueList[0] = remove_ws(div.div.strong.text)
            lis = div.ul.find_all('li')
            valueList[1] = remove_ws(lis[0].text)
            valueList[2] = remove_ws(lis[1].text)
            valueList[3] = remove_ws(lis[2].text)
            valueList[4] = remove_ws(div.find('span', class_='charge_price').text)

            print(valueList)
    except:
        raise

driver = webdriver.Chrome()
url = 'http://www.uplus.co.kr/ent/spps/chrg/RetrieveChrgList.hpi'

driver.get(url)
table = html(driver)

delay = 3
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
pageNum = soup.find('span', class_='number')
lastPageNum = int(pageNum.find_all('a')[-1].text)

for i in range(2,lastPageNum + 2):
    getList()
    for j in range(1,5):
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#svcForm > div > div.pagenavi > div > div > span.number > a:nth-child(%d)'%i)
                )
            ).click()
            break
        except IndexError:
            break
        except:
            pass

driver.close()