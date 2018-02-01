from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
from time import sleep


mainUrl = "https://course.fcu.edu.tw"


chrome_options = webdriver.ChromeOptions()

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.maximize_window()

# 帳號及密碼
username = 'd0471777'
password = ''

# 選課代號
classID = '1459'

# 確定要搶課嗎？
grabbed = True


def login():
    browser.get(mainUrl)

    cookies = browser.get_cookies()
    print('驗證碼:', cookies[2]['value'])
    # alert = browser.switch_to_alert()
    # print(alert.text)
    # alert.accept()

    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_UserName"]').send_keys(username)
    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_Password"]').send_keys(password)
    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_vcode"]').send_keys(cookies[2]['value'])
    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_LoginButton"]').click()

    print('登入成功')


def grab():
    while True:
        if browser.current_url != mainUrl:
            break
    while True:
        # select
        browser.find_element_by_xpath(
            '//*[@id="ctl00_MainContent_TabContainer1_tabSelected_Label3"]').click()

        # input class ID
        browser.find_element_by_xpath(
            '//*[@id="ctl00_MainContent_TabContainer1_tabSelected_tbSubID"]').send_keys(classID)
        browser.find_element_by_xpath(
            '//*[@id="ctl00_MainContent_TabContainer1_tabSelected_gvToAdd"]/tbody/tr[2]/td[8]/input').click()

        # alert
        sleep(0.5)
        alert = browser.switch_to_alert()

        alertInfo = alert.text
        currentValue = int(alertInfo[19:23].strip())
        openValue = int(alertInfo[25:29].strip())
        alert.accept()

        print('登記人數:', currentValue)
        print('剩餘名額:', openValue)

        if(openValue > 0 and grabbed):
            break

        browser.get(browser.current_url)

    # 選課
    if grabbed:
        browser.find_element_by_xpath(
            '//*[@id="ctl00_MainContent_TabContainer1_tabSelected_gvToAdd"]/tbody/tr[2]/td[1]/input').click()
        print('選課成功')
    sleep(10)


if __name__ == "__main__":
    login()
    grab()
    browser.close()
