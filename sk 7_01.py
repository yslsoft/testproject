from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv

def remove_ws(str):
    return str.replace('  ',' ').replace('\n\n','').replace('\t','').strip('\n ')

def totalList(li):
    file = open('SK_7mobile.csv', 'a', newline='')
    valueList = ['','','','','','','']
    name = li.find('div', class_='name')
    valueList[0] = name.find('span', class_='lb').text
    valueList[1] = name.dl.dt.text
    if name.dl.find('dd', class_='long') != None:
        valueList[2] = name.dl.find('dd', class_='long').text
        valueList[3] = valueList[2]
        valueList[4] = valueList[2]
    else :
        spans = name.dl.dd.find_all('span')
        valueList[2] = spans[0].text
        valueList[3] = spans[1].text
        valueList[4] = spans[2].text
    price = li.find('div', class_='price')
    valueList[5] = price.div.span.text.replace('  ',' ')
    if price.div.strong != None:
        valueList[6] = price.div.strong.text.replace('  ',' ')

    csvfile = csv.writer(file)
    csvfile.writerow(valueList)
    file.close()

driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.sk7mobile.com/prod/data/callingPlanList.do?refCode=LTE&searchCallPlanType=PROD_LTE_TYPE_ALL&searchOrderby=3'

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

price = soup.find('ul', class_='list-price')  #block
lis = price.find_all('li')
for li in lis:
    totalList(li)

driver.close()