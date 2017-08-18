"""Manage Website Interaction with Goerge website."""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from datetime import date, timedelta
import csv

# import time
import re


class GeorgeAccount:
    """A Class object to access George."""

    delay = 300
    de_mon_to_num = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAI': 5, 'JUN': 6,
                     'JUL': 7, 'AUG': 8, 'SEP': 9, 'OKT': 10, 'NOV': 11, 'DEZ': 12}

    def __init__(self, browser, bank_info):
        """Define all variable to access George Site."""
        self.browser = browser
        self.user = bank_info['user']
        self.password1 = bank_info['pass1']
        self.password2 = bank_info['pass2']
        self.url = "https://login.sparkasse.at/sts/oauth/authorize?response_type=token&client_id=georgeclient"
        self.george_open = False
        self.account = str(0)
        self.bank_name = "George"
        self.category_map_filename = 'GeorgeCategoryMap.csv'
        self.no_accounts = bank_info['no_accounts']
        print(self.no_accounts)
        print(self.url)

    def opensite(self):
        """Open website and place browser on  accounts page."""
        print(self.url)
        self.browser.get(self.url)
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, "user")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        self.browser.find_element_by_id("user").send_keys(self.user)
        self.browser.find_element_by_id("password").send_keys(self.password1)
        self.browser.find_element_by_id("submitButton").send_keys(Keys.RETURN)
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, "accountName")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        self.george_open = True
        return True

    def get_Saldo(self, account=0):
        """Get the account amount (user needs to know which account)."""
        account_saldo_raw = self.browser.find_elements_by_xpath('//div[@class="col-sm-3 col-xs-4 amountColumn"]')[account].text
        account_saldo_raw = account_saldo_raw.split('\n', 1)[0]
        if (account_saldo_raw[2] == "-"):
            account_negative = -1
        else:
            account_negative = 1

        account_saldo_float = (float(''.join(re.findall('\d+', account_saldo_raw)))/100)*account_negative
        account_saldo_str = str(account_saldo_float)
        account_currency = "EUR"
        saldo_return = {"bank": "George"+str(account), "saldo": account_saldo_str, "currency": account_currency}
        return(saldo_return)

    def __transaction_getstring(self, trans_no=0):
        """Select the transaction string."""
        read_success = False
        transaction_string = ""
        while(not read_success):
            try:
                transaction_string = self.browser.find_elements_by_xpath("//*[contains(@id, 'transaction-line-')]")[trans_no].text
                read_success = True
            except StaleElementReferenceException as my_err:
                print(my_err)
                pass
            return(transaction_string)

    def __get_category(self, trans_description):
        """Get a category."""
        # reader = csv.DictReader(open(self.category_map_filename, 'r'))
        reader = csv.DictReader(open('George/GeorgeCategoryMap.csv', 'r'))
        new_category = "Uncategorized"
        old_category = ""
        new_trans_description = trans_description
        for line in reader:
            if (line['Original'] in trans_description):
                new_category = line['Mapped']
                old_category = line['Original']
                new_trans_description = trans_description.replace(line['Original'], '')
                break
        return({'new': new_category, 'old': old_category, 'description': new_trans_description})

    def __parse_transaction(self, transaction_string_list):
        """Return a clearer transaction sting."""
        trans_date = date(2017, self.de_mon_to_num[transaction_string_list[1]], int(transaction_string_list[0]))
        print("I got here")
        print("Transaction lenggth is "+str(len(transaction_string_list)))

        if(len(transaction_string_list) == 5):
            trans_counterpart = transaction_string_list[2]
            trans_description = transaction_string_list[3]
            trans_amount = self.__convert_amount_2_float(transaction_string_list[4])
        elif(len(transaction_string_list) == 6):
            print(transaction_string_list)
            trans_counterpart = transaction_string_list[2]
            trans_description = transaction_string_list[3]
            trans_amount = self.__convert_amount_2_float(transaction_string_list[4])
        else:
            trans_counterpart = "Me or Bank"
            trans_description = transaction_string_list[2]
            trans_amount =self.__convert_amount_2_float(transaction_string_list[3])
        trans_account = self.bank_name+self.account

        trans_categorys = self.__get_category(trans_description)
        trans_category = trans_categorys['new']
        trans_description = trans_categorys['description']
        # Ensure orignnal category info is stored in the memo field
        trans_memo = trans_categorys['old']

        trans_FX_curr = "EUR"
        trans_FX_rate = 1.0
        return ([trans_account, trans_date, trans_amount, trans_counterpart, trans_description, trans_memo, trans_category, trans_FX_curr, trans_FX_rate, False, False])

    def __convert_amount_2_float(self, amount_string):
        amount_string = str(amount_string)
        if (amount_string[0] == '-'):
            amount = -1*(float(''.join(re.findall('\d+', str(amount_string))))/100)
        else:
            amount = (float(''.join(re.findall('\d+', str(amount_string))))/100)
        return(amount)

    def __check_date(self, transaction_string_list, delta_days=3):
        """Check that the transaction is before a certain date in relation to today."""
        early_date = date.today()-timedelta(days=delta_days)
        trans_date = date(2017, self.de_mon_to_num[transaction_string_list[1]], int(transaction_string_list[0]))
        # print(early_date)
        # print(trans_date)
        if(trans_date > early_date):
            check_date_bol = True
        else:
            check_date_bol = False
            # print(check_date_bol)
        return(check_date_bol)

    def get_transactions(self,  delta_days=3, account=0):
        """Get a list of transactions fom account from the website."""
        self.account = str(account)
        """Return a lis of transaction earlier than the given date."""

        if(account == 1):
            try:
                myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Christian T.A.P.Brenninkmeijer")))
            except TimeoutException:
                print("Loading took too much time!")
            self.browser.find_element_by_link_text("Christian T.A.P.Brenninkmeijer").click()
        elif(account == 2):
            try:
                myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.LINK_TEXT, "422093XXXXXX0412")))
            except TimeoutException:
                print("Loading took too much time!")
            self.browser.find_element_by_link_text("422093XXXXXX0412").click()
        else:
            self.browser.find_element_by_xpath("(//a[contains(text(),'Christian T.A.P.Brenninkmeijer Marc')])[2]").click()
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, "transactions")))

            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        self.browser.implicitly_wait(5)
        i = 0
        transaction_list = []
        in_date_range = True
        while (in_date_range):
            transaction_string = self.__transaction_getstring(i)
            transaction_string_list = transaction_string.splitlines()
            if(self.__check_date(transaction_string_list, delta_days)):
                transaction_list.append(self.__parse_transaction(transaction_string_list))
            else:
                print("I got here line 131")
                in_date_range = False
            i = i+1
        self.browser.find_element_by_css_selector("a.iconlink").click()
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, "accountName")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        return transaction_list
