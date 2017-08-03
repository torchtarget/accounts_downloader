from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import myencoder
import csv
import sqlite3
from datetime import date,timedelta,datetime


# import time
import re



delay = 300


def opensite(browser):
    browser.get("https://login.sparkasse.at/sts/oauth/authorize?response_type=token&client_id=georgeclient")

#   #browser.assertEqual("Erste Bank and Sparkassen Login", driver.title)
#   browser.find_element_by_xpath("//form[@id='credentials']/div/label").click()
#   browser.find_element_by_xpath("//form[@id='credentials']/div/label").click()
#    broswer.find_element_by_id("user").clear()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "user")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    browser.find_element_by_id("user").send_keys(myencoder.get_user("George"))
#   browser.find_element_by_id("password").clear()
    browser.find_element_by_id("password").send_keys(myencoder.get_pass1("George"))
    browser.find_element_by_id("submitButton").send_keys(Keys.RETURN)
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "accountName")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    return True


def get_Saldo(browser, account=0):
    #    try:
    #        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID "")))
    #        print("Page is ready!")
    #   except TimeoutException:
    #    #    print("Loading took too much time!")
    #    #    return True;

    account_saldo_raw = browser.find_elements_by_xpath('//div[@class="col-sm-3 col-xs-4 amountColumn"]')[account].text
    account_saldo_raw = account_saldo_raw.split('\n', 1)[0]
    print(account_saldo_raw[2])
    if (account_saldo_raw[2] == "-"):
        account_negative = -1
    else:
        account_negative = 1

    account_saldo_float = (float(''.join(re.findall('\d+', account_saldo_raw)))/100)*account_negative
    account_saldo_str = str(account_saldo_float)
    print(account_saldo_raw)
    account_currency="EUR"
    saldo_return = {"bank": "George"+str(account), "saldo": account_saldo_str, "currency": account_currency}
    return(saldo_return)

def transaction_getstring(browser, trans_no=0):
    read_success=False
    while(not read_success):
        try:
            transaction_string= browser.find_elements_by_xpath("//*[contains(@id, 'transaction-line-')]")[trans_no].text
            read_success=True
        except StaleElementReferenceException as my_err:
            print(my_err)
            pass
    return(transaction_string)

def parse_transaction(transaction_string=""):
    return transaction_string

def check_date(transaction_string_list,delta_days=3):
    de_mon_to_num={
    'JAN':1,
    'FEB':2,
    'MAR':3,
    'APR':4,
    'MAI':5,
    'JUN':6,
    'JUL':7,
    'AUG':8,
    'SEP':9,
    'OKT':10,
    'NOV':11,
    'DEZ':12
    }
    early_date=date.today()-timedelta(days=delta_days)
    trans_date=date(2017,de_mon_to_num[transaction_string_list[1]],int(transaction_string_list[0]))
    print(early_date)
    print(trans_date)
    if(trans_date > early_date):
        check_date_bol= True
    else:
        check_date_bol= False
    print(check_date_bol)
    return(check_date_bol)




def get_transactions(browser,account=0,delta_days=3):
    browser.find_element_by_xpath("(//a[contains(text(),'Christian T.A.P.Brenninkmeijer Marc')])[2]").click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "transactions")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    browser.implicitly_wait(5)
    i=0
    transaction_list=[]
    in_date_range=True
    while (in_date_range):
        #print(in_date_range)
        transaction_string=transaction_getstring(browser, i)
        print(transaction_string)
        transaction_string_list=transaction_string.splitlines()
        print(len(transaction_string_list))
        if(check_date(transaction_string_list,delta_days)):
            transaction_list.append(transaction_string_list)
        else:
            print("I got here line 131")
            in_date_range = False
            #print(in_date_range)
        i=i+1
        #print(in_date_range)

    # print(transaction_list_raw[0].get_attribute('innerHTML'))
    print(transaction_list[1])
    return transaction_list
