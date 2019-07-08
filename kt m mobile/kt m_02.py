from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def remove_ws(str):
    return str.replace('  ',' ').replace('\n\n','').replace('\t','').strip('\n ')

driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.ktmmobile.com/comunity/lteRateList.do?socCode=KISSLCT26'

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#요금제구분 넣기
box = soup.find_all('table', class_='__se_tbl_ext')
box1 = box[1].find_all('tr').find('td')    #box1 첫번째 요금제구분
a = box1[0].text

#클릭할것
driver.find_element_by_xpath('//*[@id="lteTable"]/div[2]/div/table/tbody/tr[1]/td[8]/button').click()
time.sleep(1)                                       #box                   #line
popup = driver.execute_script("return document.getElementsByClassName('popup_content')[0].innerHTML")
popupSoup = BeautifulSoup(popup, 'html.parser')
ktMList = []

#요금제명
title = popupSoup.find('div', class_='title')  #뒷부분 자르기(미완)
comment = title.p.text
del title.p
title = title.text
# title = remove_ws(title.text.replace(comment,''))
ktMList.append(title)

#월 기본료, 프로모션 할인
price = popupSoup.find_all('font', class_='font_small')
monthlyFe = price[0].text.replace(',','')
ktMList.append(monthlyFe)
discount = price[1].text.replace(',','')
ktMList.append(discount)

#음성, 문자, 데이터, 와이파이
tell = popupSoup.find('div', class_='tell').find('div', class_='text').text
ktMList.append(tell)
sms = popupSoup.find('div', class_='sms').find('div', class_='text').text
ktMList.append(sms)
data = popupSoup.find('div', class_='data').find('div', class_='text').text
ktMList.append(data)
wifi = popupSoup.find('div', class_='wifi').find('div', class_='text').text
ktMList.append(wifi)

#초과요율 음성, 영상, SMS, LMS, MMS, 데이터, 비고
OVER = popupSoup.find_all('tr')
over = OVER[1].find_all('td')
CALL = over[0].text
ktMList.append(CALL)
VCALL = over[1].text
ktMList.append(VCALL)
SMS = over[2].text
ktMList.append(SMS)
LMS = over[3].text
ktMList.append(LMS)
MMS = over[4].text
ktMList.append(MMS)
DATA = over[5].text
ktMList.append(DATA)
ELSE = over[6].text
ktMList.append(ELSE)

ktMList = ','.join(ktMList)

#엑셀 저장
file = open('./kt m_02.csv','w+')
file.write(ktMList)

time.sleep(1)
driver.close()