from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv

def remove_ws(str):
    return ' '.join(str.replace('\n\n','').replace('\t','').strip('\n ').split())

def getList(soupTable, sector):
    if sector == 'thead':
        fieldTag = 'th'
        soupObj = soupTable.thead

    else:
        fieldTag = 'td'
        soupObj = soupTable.tbody

    file = open('KT_M_mobile.csv', 'a', newline='')
    rowspancounts = []
    valueList = []

    line = soupObj.tr.find_all(fieldTag)
    headcolspanCount = 0
    for field in line:
        if field.get('colspan') != None:
            headcolspanCount += (int(field.get('colspan')) - 1)
    fieldCount = len(line) + headcolspanCount

    for i in range(0,fieldCount):
        rowspancounts.append(0)
        valueList.append('')

    trs = soupObj.find_all('tr')
    for tr in trs:
        fields = tr.find_all(fieldTag)
        for field in fields:
            if field.get('style') == "display: none;":
                field.clear()
            div = field.find('div',class_='rngbtn_wrap')
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

driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.ktmmobile.com/comunity/lteRateList.do?socCode=KISSLCT26'

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# box 구분하기
soupMainTable = soup.find('table', class_='__se_tbl_ext')
tables = soup.find_all('table', class_='__se_tbl_ext')
for table in tables:
    getList(table,'thead')
    getList(table,'tbody')

driver.close()