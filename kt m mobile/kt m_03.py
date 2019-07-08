from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def remove_ws(str):
    return str.replace('  ', ' ').replace('\n\n', '').replace('\t', '').strip('\n ')

driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.ktmmobile.com/comunity/lteRateList.do?socCode=KISSLCT26'

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# box 구분하기
boxs = soup.find_all('table', class_='__se_tbl_ext')
for box in boxs:
    lines = box.find_all('tr')

    spanValueList = []
    valueList = []
    headList = []
    headLine = 0
    for line in lines:

        ths = line.find_all('th')

        if line.find('th') != None:
            if rowspanValue != 0:  #rowspan이 있으면
                pass

            else:
                headLine = len(ths)

                for i in range(0, headLine):
                    spanValueList.append(0)
                    valueList.append('')
                    headList.append(ths[i].text)

            print(headList)

        else:
            tds = line.find_all('td')
            j = 0
            colspanValue = 0
            for i in range(0, headLine):
                if colspanValue == 0:
                    colspanValue = tds[j].get('colspan')
                    if colspanValue == None:
                        colspanValue = 0
                    else:
                        colspanValue = int(colspanValue) - 1

                else:
                    colspanValue -= 1
                    valueList[i] = valueList[i - 1]
                    j -= 1

                if spanValueList[i] == 0:
                    rowspanValue = tds[j].get('rowspan')
                    if rowspanValue == None:
                        rowspanValue = 0
                    else:
                        rowspanValue = int(rowspanValue) - 1
                        spanValueList[i] = rowspanValue

                    valueList[i] = tds[j].text
                    j += 1
                else:
                    spanValueList[i] -= 1

            print(valueList)
            print(spanValueList)

driver.close()