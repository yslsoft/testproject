from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


def getList(soupTable):
    # line = soup.find('tr') # soup.find('tbody').find('tr')
    spanValueList = []
    valueList = []
    headColspanValue = 0
    line = soupTable.tbody.tr.find_all('td')

    for td in line:
        if td.get('colspan') != None:
            headColspanValue += (int(td.get('colspan')) - 1)
    headLine = len(line) + headColspanValue

    for i in range(0, headLine):
        spanValueList.append(0)
        valueList.append('')
    trs = soupTable.tbody.find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')
        virtualNum = 0
        colspanValue = 0
        for i in range(0, headLine):
            if tds[virtualNum].get('style') == "display: none;":
                del tds[virtualNum]
            if colspanValue == 0:
                colspanValue = tds[virtualNum].get('colspan')
                if colspanValue == None:
                    colspanValue = 0
                else:
                    colspanValue = int(colspanValue) - 1

            else:
                colspanValue -= 1
                valueList[i] = valueList[i - 1]
                virtualNum -= 1

            if spanValueList[i] == 0:  # rowspan값 없을때
                rowspanValue = tds[virtualNum].get('rowspan')
                if rowspanValue == None:  # rowspan값 없을때
                    rowspanValue = 0
                else:  # rowspan있을떄 저장
                    rowspanValue = int(rowspanValue) - 1
                    spanValueList[i] = rowspanValue

                valueList[i] = tds[virtualNum].text
                virtualNum += 1
            else:  # rowspan값 있을떄
                spanValueList[i] -= 1

        print(valueList)
        print(spanValueList)


driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.ktmmobile.com/comunity/lteRateList.do?socCode=KISSLCT26'

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# box 구분하기
soupMainTable = soup.find('table', class_='__se_tbl_ext')
tables = soup.find_all('table', class_='__se_tbl_ext')
for table in tables:
    getList(table)

