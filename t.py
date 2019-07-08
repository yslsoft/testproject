from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
url = 'http://www.uplus.co.kr/ent/spps/chrg/RetrieveChrgList.hpi'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
number = soup.find('span', class_='number')

xpath = '//*[@id="svcForm"]/div/div[6]/div/div/span[3]/a[1]'
for i in range(1,6):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        ).click()
        print(number.find('a', href='#'))
        break
    except:
        print('x')

# def custom_wait_clickable_and_click(selector, attempts=5):
#   count = 0
#   while count < attempts:
#     try:
#       wait(1)
#       elem = wait_for_element_to_be_clickable(selector)
#       elem.click()
#       return elem