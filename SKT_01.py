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
    table = soup.find('table', class_='prd_tb')
    return table

def remove_ws(str):
    return ' '.join(str.replace('\n\n','').replace('\t','').strip('\n ').split())

def getList(soupTable, sector):
    try:
        if sector == 'thead':
            fieldTag = 'th'
            soupObj = soupTable.thead

        else:
            fieldTag = 'td'
            soupObj = soupTable.tbody

        file = open('SK텔레콤.csv', 'a', newline='')
        rowspancounts = []
        valueList = []

        line = soupObj.tr.find_all(fieldTag)
        headcolspanCount = 0
        for field in line:
            if field.get('colspan') != None:
                headcolspanCount += (int(field.get('colspan')) - 1)
        fieldCount = len(line) + headcolspanCount

        for i in range(0, fieldCount):
            rowspancounts.append(0)
            valueList.append('')

        trs = soupObj.find_all('tr')
        for tr in trs:
            fields = tr.find_all(fieldTag)
            for field in fields:
                if field.get('style') == "display: none;":
                    fields.remove(field)
                div = field.find('div', class_='rngbtn_wrap')
                if div != None:
                    div.clear()

            virtualCount = 0
            colspanCount = 0

            for fieldIndex in range(0, fieldCount):
                realNum = fieldIndex - virtualCount
                if rowspancounts[fieldIndex] == 0:
                    rowspanValue = fields[realNum].get('rowspan')
                    if rowspanValue != None:  # rowspan있을떄 저장
                        rowspancounts[fieldIndex] = int(rowspanValue) - 1

                    if colspanCount == 0:
                        colspanValue = fields[realNum].get('colspan')
                        if colspanValue != None:
                            colspanCount = int(colspanValue) - 1
                            virtualCount += 1
                    else:
                        colspanCount -= 1
                        if colspanCount > 0:
                            virtualCount += 1
                    valueList[fieldIndex] = remove_ws(fields[realNum].text)

                else:
                    rowspancounts[fieldIndex] -= 1
                    virtualCount += 1

            csvfile = csv.writer(file)
            csvfile.writerow(valueList)
        file.close()
    except:
        driver.close()
        raise


driver = webdriver.Chrome()
url = 'http://www.tworld.co.kr/normal.do?serviceId=S_PROD1102&viewId=V_PROD1102'

driver.get(url)
table = html(driver)

getList(table, 'thead')
delay = 3
for i in range(3,13):
    driver.find_element_by_css_selector('#content > div.prCont.prdNewListWrap > div.pager > div > a:nth-child(%d)'%i).click()
    try:
        WebDriverWait(driver, delay).until(EC.invisibility_of_element((By.TAG_NAME, "#table")))
        table = html(driver)
    except:
        print('태그가 확인되지않습니다.')
        raise
    getList(table, 'tbody')
driver.find_element_by_css_selector('#content > div.prCont.prdNewListWrap > div.pager > div > a.btn.next').click()
table = html(driver)
getList(table, 'tbody')

driver.close()