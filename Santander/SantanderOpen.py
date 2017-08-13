import time, re

import myencoder
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


delay=300
def opensite(browser):
    #browser = webdriver.Firefox()
    #browser.find_element_by_css_selector("span.logon-span").click()
    #browser.find_element_by_link_text("Personal Internet BankingOpens in a new Window.").click()

    browser.get("http://www.santander.com.mx/mx/home/")
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = browser.current_window_handle
        #browser.assertEqual("Banco Santander", driver.title)

    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.mypass.masked")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    browser.find_element_by_css_selector("input.mypass.masked").clear()
    browser.find_element_by_css_selector("input.mypass.masked").send_keys(myencoder.get_user("Santander"))
    try:
        myElem = WebDriverWait(browser,1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "kill-gfx")))
        browser.find_element_by_css_selector("kill-gfx").click()
    except TimeoutException:
        print("Loading took too much time!")


    browser.find_element_by_id("splg.btnEntrar").send_keys(Keys.RETURN)


    signin_window_handle = None
    while not signin_window_handle:
        for handle in browser.window_handles:
            if handle != main_window_handle:
                signin_window_handle = handle
                print("gotnewwindow")
                print(handle)
                break
    browser.switch_to.window(signin_window_handle)

    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "stu.nip")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    browser.find_element_by_id("stu.nip").clear()
    browser.find_element_by_id("stu.nip").send_keys(myencoder.get_pass("Santander"))
    browser.find_element_by_xpath("//a[@id='login.Continuar']/span").click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "summ.rowCCP0.i6")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    return True;



def get_Saldo(browser,account=0):
    if(account==0):
        account_saldo=browser.find_element_by_id("summ.rowCCP0.i6").text
        account_currency="MXN"
    elif(account==1):
        account_saldo=browser.find_element_by_xpath("//td[@id='rowFCCP.i6']/b").text
        account_currency="MXN"

        #Gets all the digits, converts to float and divides by 100
    account_saldo_float=float(''.join(re.findall('\d+',account_saldo)))/100
    account_saldo_str=str(account_saldo_float)
    saldo_return={"bank":"Santander"+str(account),"saldo":account_saldo_str,"currency":account_currency}
    return(saldo_return)
